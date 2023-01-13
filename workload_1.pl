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
my %isFacultyAssigned;

sub min {
	my (@n) = @_;
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
	
	#Course assignment status
	$isFacultyAssigned{$emp_id} = 0;
	
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
	
	my @preferenceNumber = (1..4);
	for my $i (@preferenceNumber) {
		foreach (keys %instructorRequirement) {
			my $reqdNumber = $instructorRequirement{$_};
			if ($reqdNumber == 0){next;}
			
			my $numberFaculty;
			my @reqdFacultyList;
			if ($preference{$_}{$i}) {
				my @optedFaculty = @{$preference{$_}{$i}};
				# print "Course number:",$_,"\n";
				# print $_,"\t" foreach (@optedFaculty); print "\n";
				
				my @updatedOptedFaculty;
				# Skip faculty already assigned
				for my $currFaculty (@optedFaculty){
					if ($isFacultyAssigned{$currFaculty} == 0){
						push @updatedOptedFaculty,$currFaculty;
					}
				}
				# print "Updated faculty list:","\n";
				# print $_,"\t",$isFacultyAssigned{$_},"\t" foreach (@updatedOptedFaculty); print "\n";
				
				$numberFaculty = @updatedOptedFaculty;
				@reqdFacultyList = @updatedOptedFaculty[0 .. min($reqdNumber,$numberFaculty)-1];
				# print $_,"\n" foreach @reqdFacultyList;
				$courseFacultyMap{$_} = \@reqdFacultyList;
			}
			else {$numberFaculty = 0;}
		
			# Update assignment status for allotted faculty
			foreach (@reqdFacultyList) {
				$isFacultyAssigned{$_} = 1;
			}
			
			# # DEBUGG
# 			foreach (keys %isFacultyAssigned){
# 				print $_," ",$isFacultyAssigned{$_},"\t";
# 			}
# 			print "\n";
		
			# Update reqdNumber
			$reqdNumber = $reqdNumber - min($reqdNumber,$numberFaculty);
			$instructorRequirement{$_} = $reqdNumber;
		}
	}
	
	# Check information populated
	foreach (keys %instructorRequirement) {
		my @assignedFaculty = @{$courseFacultyMap{$_}};
		print $_,"\t",@assignedFaculty,"\n";
		print "Updated requirement:",$instructorRequirement{$_},"\n"; 
	}			
	
}

sub printInfo {
	open(PREF,">coursePreference.csv");
	my @preferenceNumber = (1..4);
	foreach (keys %preference) {
		print PREF "\n",$_;
		for my $i (@preferenceNumber){
			print PREF "\nOption",$i,": ";
			if ($preference{$_}{$i}) {
				my @optedFaculty = @{$preference{$_}{$i}};
				print PREF $_," " foreach(@optedFaculty);
			}
		}		
	}
	close (PREF);
}

# Main routine
# Create hash map of courseNames, preference order, and empID
foreach $line (@data) {
	course_preference_list($line);
	# print $_,"\t" foreach @{$preference{"MA1101: Functions of Several Variables"}{4}},"\n";
}
print Dumper(\%preference);

# Create hash map of courseNames and requirement
populateCourseRequirement();

# Allot courses
allotCourses();

# Print Info
printInfo();
