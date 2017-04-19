<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $lname = $_POST['rmlocation'];

  $result = $conn->query("SELECT * FROM locationinfo WHERE locationname = '$lname'");

  if($result){
    if($result->num_rows <= 0){
      echo "<h1>location does not exists</h1>";
    }
    else {
      $result = $conn->query("DELETE FROM locationinfo WHERE locationname = '$lname'");
      if($result) {
        echo "<h1>Successfully removed location</h1>";
      }
      else {
        echo "<h1>Failed to delete location</h1></br>";
        echo $result;
      }
    }
  }
 ?>
