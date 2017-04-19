<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $tid = $_POST['addtroughid'];

  $result = $conn->query("SELECT * FROM troughinfo WHERE troughid = $tid");

  if($result){
    if($result->num_rows > 0){
      echo "<h1>Trough id already exists</h1>";
    }
    else {
      $result = $conn->query("INSERT INTO troughinfo(troughid) VALUES ($tid)");
      if($result) {
        echo "<h1>Successfully added new troughid</h1>";
      }
      else {
        echo "<h1>Failed to insert new trough id</h1></br>";
        echo $result;
      }
    }
  }
 ?>
