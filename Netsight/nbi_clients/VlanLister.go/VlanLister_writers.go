package main

/*
#### ##     ## ########   #######  ########  ########  ######
 ##  ###   ### ##     ## ##     ## ##     ##    ##    ##    ##
 ##  #### #### ##     ## ##     ## ##     ##    ##    ##
 ##  ## ### ## ########  ##     ## ########     ##     ######
 ##  ##     ## ##        ##     ## ##   ##      ##          ##
 ##  ##     ## ##        ##     ## ##    ##     ##    ##    ##
#### ##     ## ##         #######  ##     ##    ##     ######
*/

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"

	excelize "github.com/360EntSecGroup-Skylar/excelize"
)

/*
##     ##    ###    ########   ######
##     ##   ## ##   ##     ## ##    ##
##     ##  ##   ##  ##     ## ##
##     ## ##     ## ########   ######
 ##   ##  ######### ##   ##         ##
  ## ##   ##     ## ##    ##  ##    ##
   ###    ##     ## ##     ##  ######
*/

var (
	// Columns used in outfiles
	tableColumns = [...]string{"ID", "BaseMac", "IP", "SysUpDown", "SysName", "SysLocation", "IfName", "IfStatus", "Untagged", "Tagged"}
	// File types that are valid for writing
	validFiletypes = [...]string{"csv", "stdout", "xlsx"}
)

/*
######## ##     ## ##    ##  ######   ######
##       ##     ## ###   ## ##    ## ##    ##
##       ##     ## ####  ## ##       ##
######   ##     ## ## ## ## ##        ######
##       ##     ## ##  #### ##             ##
##       ##     ## ##   ### ##    ## ##    ##
##        #######  ##    ##  ######   ######
*/

// Transforms an array of resultSets to CSV data
func rsArrayToCSV(results []resultSet) (uint, string) {
	var rowsWritten uint = 0
	var rowData string
	var csvData string = ""

	for _, row := range results {
		rowData = ""
		for _, element := range row.ToArray() {
			rowData = fmt.Sprintf("%s,\"%s\"", rowData, element)
		}
		csvData = fmt.Sprintf("%s%s\n", csvData, strings.TrimPrefix(rowData, ","))
		rowsWritten++
	}

	return rowsWritten, csvData
}

// Decides which actual writeResults* function shall be used based on filename pre- or suffix
func writeResults(filename string, results []resultSet) (uint, error) {
	// Prefix checking
	for _, filetype := range validFiletypes {
		prefix := fmt.Sprintf("%s:", filetype)
		if strings.HasPrefix(filename, prefix) {
			filename = strings.TrimPrefix(filename, prefix)
			switch filetype {
			case "csv":
				return writeResultsCSV(filename, results)
			case "stdout":
				return writeResultsStdout(filename, results)
			case "xlsx":
				return writeResultsXLSX(filename, results)
			}
		}
	}

	// Suffix checking
	for _, filetype := range validFiletypes {
		suffix := fmt.Sprintf(".%s", filetype)
		if strings.HasSuffix(filename, suffix) {
			switch filetype {
			case "csv":
				return writeResultsCSV(filename, results)
			case "stdout":
				return writeResultsStdout(filename, results)
			case "xlsx":
				return writeResultsXLSX(filename, results)
			}
		}
	}

	return 0, fmt.Errorf("Could not determine file type for <%s>", filename)
}

// Writes the results to outfile in CSV format
func writeResultsCSV(filename string, results []resultSet) (uint, error) {
	var rowsWritten uint = 0
	var rowData string

	fileHandle, fileErr := os.Create(filename)
	if fileErr != nil {
		return rowsWritten, fmt.Errorf("Could not write outfile: %s", fileErr)
	}
	fileWriter := bufio.NewWriter(fileHandle)
	_, writeErr := fileWriter.WriteString(fmt.Sprintf("%s\n", strings.Join(tableColumns[0:10], ",")))
	if writeErr != nil {
		return rowsWritten, fmt.Errorf("Could not write outfile: %s", writeErr)
	}
	for _, row := range results {
		rowData = ""
		for _, element := range row.ToArray() {
			rowData = fmt.Sprintf("%s,\"%s\"", rowData, element)
		}
		rowData = fmt.Sprintf("%s\n", strings.TrimPrefix(rowData, ","))
		_, writeErr := fileWriter.WriteString(rowData)
		if writeErr != nil {
			return rowsWritten, fmt.Errorf("Could not write outfile: %s", writeErr)
		}
		flushErr := fileWriter.Flush()
		if flushErr != nil {
			stdErr.Printf("Could not flush file buffer: %s\n", flushErr)
		}
		rowsWritten++
	}
	syncErr := fileHandle.Sync()
	if syncErr != nil {
		stdErr.Printf("Could not sync file handle: %s\n", syncErr)
	}
	fhErr := fileHandle.Close()
	if fhErr != nil {
		stdErr.Printf("Could not close file handle: %s\n", fhErr)
	}

	return rowsWritten, nil
}

// Writes the results to stdout in CSV format
func writeResultsStdout(filename string, results []resultSet) (uint, error) {
	rowsWritten, csvData := rsArrayToCSV(results)
	fmt.Print(csvData)
	return rowsWritten, nil
}

// Writes the results to outfile in XLSX format
func writeResultsXLSX(filename string, results []resultSet) (uint, error) {
	var rowsWritten uint = 0
	var colIndex int = 1
	var rowIndex int = 1

	xlsx := excelize.NewFile()

	for _, columnName := range tableColumns {
		position, positionErr := excelize.CoordinatesToCellName(colIndex, rowIndex)
		if positionErr != nil {
			return rowsWritten, positionErr
		}
		valueErr := xlsx.SetCellValue("Sheet1", position, columnName)
		if valueErr != nil {
			stdErr.Printf("Could not set value for %s: %s", position, valueErr)
		}
		colIndex++
	}

	for _, row := range results {
		colIndex = 1
		rowIndex++
		for _, element := range row.ToArray() {
			position, positionErr := excelize.CoordinatesToCellName(colIndex, rowIndex)
			if positionErr != nil {
				return rowsWritten, positionErr
			}
			valueErr := xlsx.SetCellValue("Sheet1", position, element)
			if valueErr != nil {
				stdErr.Printf("Could not set value for %s: %s", position, valueErr)
			}
			colIndex++
		}
		rowsWritten++
	}

	xlsx.SetSheetName("Sheet1", time.Now().Format(time.RFC3339))

	if saveErr := xlsx.SaveAs(filename); saveErr != nil {
		return rowsWritten, saveErr
	}

	return rowsWritten, nil
}
