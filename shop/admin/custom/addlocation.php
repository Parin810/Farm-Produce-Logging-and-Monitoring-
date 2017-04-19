<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $lname = $_POST['addlocation'];

  $result = $conn->query("SELECT * FROM locationinfo WHERE locationname = '$lname'");

  if($result){
    if($result->num_rows > 0){
      echo "<h1>Location already exists</h1>";
    }
    else {
      $result = $conn->query("INSERT INTO locationinfo(locationname) VALUES ('$lname')");
      if($result) {
        echo "<h1>Successfully added new location</h1>";
      }
      else {
        echo "<h1>Failed to insert new location</h1></br>";
        echo $result;
      }
    }
  }
 ?>
