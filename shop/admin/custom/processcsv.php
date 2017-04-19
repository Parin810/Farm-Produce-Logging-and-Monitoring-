<?php

// output headers so that the file is downloaded rather than displayed
header('Content-Type: text/csv; charset=utf-8');
header('Content-Disposition: attachment; filename=data.csv');

// create a file pointer connected to the output stream
$output = fopen('php://output', 'w');

// output the column headings
fputcsv($output, array('Date and Time', 'Trough ID', 'Name', 'Weight', 'Location'));

$conn = new mysqli("localhost", "root", "", "opencart");

if($conn->connect_error){
  echo "$conn->connect_error";
}
$sd = $_POST['startdate'];
$ed = $_POST['enddate'];
$q = "SELECT date,troughid,name,weight,location FROM data WHERE date BETWEEN '$sd' AND '$ed'";
// echo $q;
$result = $conn->query($q);
 while($row = $result->fetch_assoc()){
   fputcsv($output, $row);
 }
?>
