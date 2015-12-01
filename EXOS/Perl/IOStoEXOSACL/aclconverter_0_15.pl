#!/usr/bin/perl
# ACL to EXOS POLICY CONVERTER version 0.15
# License:
# *******************************
# Copyright (c) 2015, Extreme Networks
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Support
# ******************************
# The software is provided as is and Extreme has no obligation to provide
# maintenance, support, updates, enhancements or modifications.
# Any support provided by Extreme is at its sole discretion.
# Issues and/or bug fixes may be reported in the Hub:
#
# https://community.extremenetworks.com/extreme
#
###
##
##  perl -w aclconverter.pl {aclfilename} [-c] [> outputfile]
##
##  where the [-c] option means "compressed"
##
##  Example:
##  perl -w aclconverter.pl sample.acl -c >  sampleacl.pol
##
##  The above example results in a compressed policy file (no indents, one \n)
##
## This version adds support for remark line conversion.
######
sub portarray;
sub typearray;
sub codearray;
sub printentry;

# Main:
#-------------------------------------------------------------------------------
use strict;
die "No Filename!" unless defined (my $filename = $ARGV[0]);
my $comp = 0;
if (defined $ARGV[1]) {
$comp = ($ARGV[1] =~ m/\-c/);
}
my $nextln = "\n";
my $smspacer = "   ";
my $spacer = "      ";
if ($comp == 1) {
   $nextln = " ";
   $spacer = "";
   $smspacer = " ";
}
my @ports;
my @types;
my @codes;
my $lineno = 1;
my $element;
my $elnum = 0;
my $named = 0;
my $name = "";
my $num  = 0;
my $extd = 0;
my $action = "";
my $actmod = "";
my $conmod = "";
my $proto = "";
my $sa = "";
my $da = "";
my $sm = "";
my $dm = "";
my $sp = "";
my $dp = "";
my $line;
my @eline;
my @line;
my $fln;
my $fname;
my $fno;
my $fcno;
open (ACLFILE, "$filename") || die "ACL file not found in directory.\n";
$line = <ACLFILE> || die "Unexpected end of ACL lines.\n";
$named = ($line =~ m/ip\saccess\-list/);
@line = split (/\s+/, $line);
if ($named == 1) {
   $name = pop (@line);
   $extd = ($line =~ m/extended/);
} else {
   $num = $line[1];
   $extd = ((($num > 99) && ($num < 1300)) || (($num > 1999) && ($num < 2000))) or $extd = 0;
   $name = "acl_$num";
}
close ACLFILE;
open (ACLFILE, "$filename") || die "ACL file not found in directory.\n";
while ($line = <ACLFILE>) {
   if ($named == 1 && $lineno == 1){
      $line = <ACLFILE> || die "Unexpected end of ACL lines.\n";
   }
   $line =~ s/\t+//;
   $line =~ s/\s{2,}//;
   if ($line =~ s/remark/#/) {
      $line =~ s/ # /#/;
      print "$line";
   } else {
      if ($line =~ s/dscp//){
         die "dscp condition not supported\n";
      }
      if ($line =~ s/dynamic//){
      die "dynamic condition not supported\n";
      }
      if ($line =~ s/ttl//){
      die "ttl condition not supported\n";
      }
      if ($line =~ s/log-input//){
         die "log-input condition not supported\n";
      }
      if ($line =~ s/reflect//){
         die "reflect condition not supported\n";
      }
      if ($line =~ s/time-range//){
         die "time-range condition not supported\n";
      }
      if ($line =~ s/precedence//){
         die "precedence condition not supported\n";
      }
      if ($line =~ s/option//){
         die "option condition not supported\n";
      }
      $line =~ s/\soperator//; # We don't need this to recognise SP/DP.
      $line =~ s/access\-list\s$num//;
      if ($line =~ s/(permit)// || $line =~ s/(deny)//) {
         $action = $1;
      }
      $line =~ s/(host\s)([0-9]+\.)([0-9]+\.)([0-9]+\.)([0-9]+)/$2$3$4$5\/32/g;
      if ($extd == 1) {
         $line =~ s/ip\s//;
         if ($line =~ s/tcp\s//) {
            $proto = "tcp";
            if ($line =~ s/established//){
#            $conmod = $conmod."TCP-flags RST \;".$nextln.$spacer."TCP-flags ACK \;".$nextln;
               $conmod = "EST";
            }
         }
         if ($line =~ s/udp\s//) {
            $proto = "udp";
         }
         if ($line =~ s/icmp\s//) {
            $proto = "icmp";
            my @types = typearray();
            while ($fln = shift(@types)) {
               ($fname, $fno) = split (/\s/,$fln);
               if ($line =~ s/\s$fname//) {
                  $conmod = $conmod."ICMP-type $fno \;".$nextln;
               }
            }
            @codes = codearray();
            while ($fln = shift (@codes)) {
               ($fname, $fno, $fcno) = split (/\s/,$fln);
               if ($line =~ s/$fname//) {
                  $conmod = $conmod."ICMP-type $fno \;".$nextln.$spacer."ICMP-code $fcno \;".$nextln;
               }
            }
            if ($line =~ s/(\s[0-9]+)(\s[0-9]+)\s//) {
               $conmod = $conmod."ICMP-type$1 \;".$nextln.$spacer."ICMP-code$2 \;".$nextln;
            }
         }
         $line =~ s/(range\s)([0-9]+)\s([0-9]+)/port_rg_$2\-$3/g;
         my @ports = portarray();
         while ($fln = shift (@ports)) {
            ($fname, $fno) = split (/\s/,$fln);
            $line =~ s/$fname/$fno/;
         }
         $line =~ s/([0-9]+\.)([0-9]+\.)([0-9]+\.)([0-9]+\s)([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)/$1.$2.$3.$4."mask_".(255-$5)."\.".(255-$6)."\.".(255-$7)."\.".(255-$8)/eg;
         if ($line =~ s/log//){
            $actmod = $actmod."log \;".$nextln;
         }
         if ($line =~ s/fragments//){
            $conmod = $conmod."fragments \;".$nextln;
         }
         if ($line =~ s/tos\s([0-9]+)//){
            $conmod = $conmod."IP-TOS $1 \;".$nextln;
         }
         $line =~ s/gt\s/port_gt_/g;
         $line =~ s/lt\s/port_lt_/g;
         $line =~ s/neq\s([0-9]+)/port_neq_$1/g;
         $line =~ s/eq\s([0-9]+)/port_eq_$1/g;
         $line =~ s/^\s+//;
         $line =~ s/\s+$//;
         if ($line =~ s/igmp\s//) {
            $proto = "igmp";
            if ($line =~ s/\s([0-9]+)$//) {
               $conmod = "IGMP-msg-type $1 \;".$nextln.$conmod;
            }
         }
         if ($line  =~ s/ahp\s//){
            $proto = "51";
         }
         if ($line =~ s/eigrp\s//){
            $proto = "88";
         }
         if ($line =~ s/esp\s//){
            $proto = "50";
         }
         if ($line =~ s/gre\s//){
            $proto = "47";
         }
         if ($line =~ s/ipinip\s//){
            $proto = "94";
         }
         if ($line =~ s/nos\s//){
            $proto = "47";
         }
         if ($line =~ s/object-group\s//){
            $proto = "53";
         }
         if ($line =~ s/ospf\s//){
            $proto = "89";
         }
         if ($line =~ s/pcp\s//){
            $proto = "108";
         }
         if ($line =~ s/pim\s//){
            $proto = "103";
         }
         if ($line =~ s/^([0-9]+)\s//){
            $proto = "$1";
         }
         @eline = split(/ /,$line);
         while ($element = shift (@eline)) {
            $elnum++;
            if ($element =~ m/(^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$)/ || $element =~ m/(^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/32$)/) {
               if ($elnum == 1) {
                  $sa = ($1);
               } else {
                  $da = ($1);
               }
            }
            if ($element =~ s/^mask\_([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)$//) {
               if ($elnum == 2) {
                  $sm = ($1);
               } else {
                  $dm = ($1);
               }
            }
            if ($element =~ m/port/) {
               if ($element =~s/^port\_([a-z]+)\_([0-9]+\-[0-9]+$)// || $element =~s/port\_([a-z]+)\_([0-9]+$)//) {
                  if ($elnum == 3 && $sm ne "") {
                     $sp = $1." ".$2;
                  } elsif ($elnum > 2) {
                     $dp = $1." ".$2;
                  } else {
                     $sp = $1." ".$2;
                  }
                  $sp =~ s/\seq\s//;
                  $sp =~ s/rg\s//;
                  $dp =~ s/\seq\s//;
                  $dp =~ s/rg\s//;
               }
            }
         }
      } else {
         $line =~ s/^\s+//;
         $line =~ s/\s+$//;
         if ($line =~ s/([0-9]+\.)([0-9]+\.)([0-9]+\.)([0-9]+\s)([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+$)/$1.$2.$3.$4."\_".(255-$5)."\.".(255-$6)."\.".(255-$7)."\.".(255-$8)/e) {
            ($sa,$sm) = split (/\_/,$line);
         } elsif ($line =~ s/host\s([0-9]+\.)([0-9]+\.)([0-9]+\.)([0-9]+)/$1$2$3$4/g || $line =~ s/([0-9]+\.)([0-9]+\.)([0-9]+\.)([0-9]+)/$1$2$3$4/g) {
            $sa = $1.$2.$3.$4."\/32";
         }
      }
      if ( $conmod =~ m/^EST$/ ) {
         my $oldname = $name;
         $name = $oldname."_RST";
         $conmod = "TCP-flags RST \;";
         printentry();
         $name = $oldname."_RST_ACK";
         $conmod = "TCP-flags 0x14 \;";
         printentry();
         $name = $oldname."_SYN_ACK";
         $conmod = "TCP-flags SYN_ACK \;";
         printentry();
         $name = $oldname."_ACK";
         $conmod = "TCP-flags ACK \;";
         printentry();
         $name = $oldname."_PSH_ACK";
         $conmod = "TCP-flags 0x18 \;";
         printentry();
         $name = $oldname."_FIN_ACK";
         $conmod = "TCP-flags 0x11 \;";
         printentry();
         $name = $oldname;
      } else {
         printentry();
      }
      $action = "";
      $actmod = "";
      $conmod = "";
      $proto = "";
      $sa = "";
      $da = "";
      $sm = "";
      $dm = "";
      $sp = "";
      $dp = "";
      $lineno++;
      $conmod = "";
      $actmod = "";
      $elnum = 0;
   }
}
close ACLFILE;
exit 0;

sub printentry {

   print "entry $name\_$lineno {$nextln";
   print $smspacer."if {$nextln";
   if ($proto ne "") {
      print $spacer."protocol $proto \;$nextln";
   }
   if ($sa ne "") {
      print $spacer."source-address $sa";
      if ($sm ne "") {
         print " mask $sm";
      }
      print " \;$nextln";
   }
   if ($sp ne "") {
      print $spacer."source-port $sp \;$nextln";
   }
   if ($da ne "") {
      print $spacer."destination-address $da";
      if ($dm ne "") {
         print " mask $dm";
      }
      print " \;$nextln"
   }
   if ($dp ne "") {
      print $spacer."destination-port $dp \;$nextln";
   }
   if ($conmod ne "") {
      print $spacer."$conmod";
   }
   print $smspacer."} then {$nextln";
   if ($action ne "") {
      print $spacer."$action \;$nextln";
   }
   if ($actmod ne "") {
      print $spacer."$actmod";
   }
   print $smspacer."}$nextln";
   print "}\n";
}

sub portarray {

   my @ports;

   push (@ports,
      'bgp 179',
      'chargen 19',
      'cmd 514',
      'daytime 13',
      'discard 9',
      'domain 53',
      'drip 3949',
      'echo 7',
      'exec 512',
      'finger 79',
      'ftp 21',
      'ftp-data 20',
      'gopher 70',
      'hostname 101',
      'ident 113',
      'irc 194',
      'klogin 543',
      'kshell 544',
      'login 513',
      'lpd 515',
      'nntp 119',
      'pim-auto-rp 496',
      'pop2 109',
      'pop3 110',
      'smtp 25',
      'sunrpc 111',
      'tacacs 49',
      'talk 517',
      'telnet 23',
      'time 37',
      'uucp 540',
      'whois 43',
      'www 80',
      'biff 512',
      'bootpc 68',
      'bootps 69',
      'discard 9',
      'dnsix 195',
      'domain 53',
      'echo 7',
      'isakmp 500',
      'mobile-ip 434',
      'nameserver 42',
      'netbios-dgm 138',
      'netbios-ns 137',
      'netbios-ss 139',
      'non500-isakmp 4500',
      'ntp 123',
      'pim-auto-rp 496',
      'rip 520',
      'snmp 161',
      'snmptrap 162',
      'sunrpc 111',
      'syslog 514',
      'tacacs 49',
      'talk 517',
      'tftp 69',
      'time 37',
      'who 513',
      'xdmcp 177');
   return @ports;
}

sub typearray {

   my @types;

   push (@types,
      'echo-reply 0',
      'unreachable 3',
      'source-quench 4',
      'redirect 5',
      'alternate-address 6',
      'echo 8',
      'router-advertisement 9',
      'router-solicitation 10',
      'time-exceeded 11',
      'parameter-problem 12',
      'timestamp-request 13',
      'timestamp-reply 14',
      'information-request 15',
      'information-reply 16',
      'mask-request 17',
      'mask-reply 18',
      'traceroute 30',
      'conversion-error 31',
      'mobile-redirect 32');

   return @types;

}

sub codearray {

   my @codes;

   push (@codes,
      'net-unreachable 3 0',
      'host-unreachable 3 1',
      'protocol-unreachable 3 2',
      'port-unreachable 3 3',
      'packet-too-big 3 4',
      'source-route-failed 3 5',
      'network-unknown 3 6',
      'host-unknown 3 7',
      'host-isolated 3 8',
      'dod-net-prohibited 3 9',
      'dod-host-prohibited 3 10',
      'net-tos-unreachable 3 11',
      'host-tos-unreachable 3 12',
      'administratively-prohibited 3 13',
      'net-redirect 5 0',
      'host-redirect 5 1',
      'net-tos-redirect 5 2',
      'host-tos-redirect 5 3',
      'ttl-exceeded 11 0',
      'reassembly-timeout 11 1',
      'option-missing 12 1',
      'no-room-for-option 12 2',
      'precedence-unreachable ERROR ERROR');

   return @codes;
}
