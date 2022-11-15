#!/usr/bin/perl -w
use strict;
#my @sample_list=("D028_13", "D027_13", "D026_13", "D021_13", "D019_13", "D018_13", "D017_13", "D013_13", "D009_13","D005_13", "D030_13", "19_D019", "19_D011", "19_D010","19_D009", "19_D008",  "19_D007", "19_D006","19_D005","19_D003");
my $sample_list = "/storage/chenlab/Users/junwang/human_meta/data/donor_all_batch_new_celltype_num";
my %sample;
open(INPUT,$sample_list);
my $header = <INPUT>;
chomp $header;
my @sample_list1 = split(/\,/,$header);
my @sample_list = @sample_list1; #@sample_list1[0..30];
while(my $line = <INPUT>){
chomp $line;
my @info = split(/\,/,$line);
for(my $i=1; $i<=$#info; $i++){
#if($info[$i]>=40){

if($info[$i]>=100){
$sample{$info[0]}->{$sample_list[$i]}=$info[$i];
}
}
}

#my @ct_name = ("Rod");
my @ct_name = ("Rod","AC","BC","Cone","HC","MG","RGC","Astrocyte");

#my @ct_name = ("AC","BC","Cone","HC","MG","RGC","Rod","Astrocyte","Microglia","RPE");
my %people;
for(my $s=1;$s<=$#sample_list;$s++){
my $sam = $sample_list[$s];

my $file="/storage/chenlab/Users/junwang/human_meta/data/genexp_donor_raw_batch_new/$sam".".txt.gz";

open(INPUT,"gunzip -c $file|");
my $line = <INPUT>;
chomp $line;
my @ct = split(/\s+/,$line);
while(my $line = <INPUT>){
chomp $line;
my @info = split(/\s+/,$line);
for(my $i=1; $i<=$#info;$i++){
$people{$ct[$i]}->{$info[0]}->{$sam} = $info[$i];
}
}
}
`mkdir /storage/chenlab/Users/junwang/human_meta/data/genexp_donor_cell_raw_batch_new`;

for my $key (keys %people){
if(($key eq "unassigned")) {#||($key eq "Rod")){
next;
}
my $output = "/storage/chenlab/Users/junwang/human_meta/data/genexp_donor_cell_raw_batch_new/exp_"."$key";

open(OUTPUT,">$output");
my @sample_ct = sort (keys %{$sample{$key}});
my $header = join("\t",@sample_ct);
print OUTPUT "$header\n";
for my $gene (sort keys %{$people{$key}}){
my $zero_gene=0;
    for(my $i=0; $i<=$#sample_ct-1; $i++){
        if(!(defined $people{$key}->{$gene}->{$sample_ct[$i]})){
#                  $people{$key}->{$gene}->{$sample_ct[$i]}=0;
        $zero_gene++;                  
        }
#     print OUTPUT "$people{$key}->{$gene}->{$sample_ct[$i]}\t";
    }

if($zero_gene==0){
print OUTPUT "$gene\t";

    for(my $i=0; $i<=$#sample_ct-1; $i++){
        if(!(defined $people{$key}->{$gene}->{$sample_ct[$i]})){
                  $people{$key}->{$gene}->{$sample_ct[$i]}=0;
        }
     print OUTPUT "$people{$key}->{$gene}->{$sample_ct[$i]}\t";
    }
#}


  my $tmp = $#sample_ct;
  if(!(defined $sample_ct[$#sample_ct])){
  print "$key\t$tmp\n";
  exit;
  }
  if(!(defined $people{$key}->{$gene}->{$sample_ct[$#sample_ct]})){
                  $people{$key}->{$gene}->{$sample_ct[$#sample_ct]}=0;
   }
     print OUTPUT "$people{$key}->{$gene}->{$sample_ct[$#sample_ct]}\n";
}
}
}
