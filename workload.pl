#!/usr/bin/perl -w 
use Data::Dumper;

open(DATA,"Teaching_Preference.csv");
my @data = <DATA>;
shift(@data);
close (DATA);

open(REQ,"facultyRequirement.csv");
my @requirement = <REQ>;
close (REQ);

my %preference; 
my %instructorRequirement;
my %courseFacultyMap;

sub min {
	@n = @_;
	if ($n[0]<$n[1]) {
		return $n[0];
	}
	else {
		return $n[1];
	}
}
sub course_preference_list {
	my ($priority) = @_;
	my @ipriority = split("\",\"",$priority);
	
	my $emp_id 			= ($ipriority[1]);
	my $first_option 	= substr($ipriority[2], 0, 6);
	my $second_option 	= substr($ipriority[3], 0, 6);
	my $third_option 	= substr($ipriority[4], 0, 6);
	my $fourth_option 	= substr($ipriority[5], 0, 6);
	# print $emp_id,"\t",$first_option,"\t",$second_option,"\n";
	
	#First course option

	my @empID1;
	if ($preference{$first_option}{1}){
		@empID1 = @{$preference{$first_option}{1}};
	}
	push (@empID1,$emp_id);
    $preference{$first_option}{1} = \@empID1;
	# print $_,"\t" foreach (@{$preference{$first_option}{1}});

	
	my @empID2;
	if ($preference{$second_option}{2}){
		@empID2 = @{$preference{$second_option}{2}};
	}
	push (@empID2,$emp_id);
    $preference{$second_option}{2} = \@empID2;
	# print $_,"\t" foreach (@{$preference{$second_option}{2}});

	my @empID3;
	if ($preference{$third_option}{3}){
		@empID3 = @{$preference{$third_option}{3}};
	}
	push (@empID3,$emp_id);
    $preference{$third_option}{3} = \@empID3;
	# print $_,"\t" foreach (@{$preference{$third_option}{3}});

	
	my @empID4;
	if ($preference{$fourth_option}{4}){
		@empID4 = @{$preference{$fourth_option}{4}};
	}
	push (@empID4,$emp_id);
	$preference{$fourth_option}{4} = \@empID4;
	# print $_,"\t" foreach (@{$preference{$fourth_option}{4}});
	
	# open(COURSE, ">>output/ratings.txt");
	# print COURSE $emp_id, "\t";
	# print COURSE $first_option, "\t";
	# print COURSE $second_option, "\t";
	# print COURSE $third_option, "\n";
	# print COURSE $fourth_option, "\n";
	# close(COURSE);
}

sub populateCourseRequirement {
	my @courses = keys %preference;
	# print $_,"\t" foreach(@courses);
	# print "\n";
	foreach (@requirement) {
		my @details = split(" ",$_);
		$instructorRequirement{$details[0]} = $details[1];
	}
	# print Dumper(\%instructorRequirement);
}

sub allotCourses {
	foreach (keys %instructorRequirement) {
		my $reqdNumber = $instructorRequirement{$_};
		if ($preference{$_}{1}) {
			my @optedFaculty = @{$preference{$_}{1}};
			my $numberFaculty = @optedFaculty;
			# if ($reqdNumber <= $numberFaculty) {
				my @reqdFacultyList = @optedFaculty[0 .. min($reqdNumber,$numberFaculty)-1];
				print $_,"\n" foreach @reqdFacultyList;
			# }
		}
	}
}

# Main routine
# Create hash map of courseNames, preference order, and empID
foreach $line (@data) {
	course_preference_list($line);
	# print $_,"\t" foreach @{$preference{"MA1101: Functions of Several Variables"}{4}},"\n";
}
# print Dumper(\%preference);

# Create hash map of courseNames and requirement
populateCourseRequirement();

# Allot courses
allotCourses();