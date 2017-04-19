<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $tid = $_POST['rmtroughid'];

  $result = $conn->query("SELECT * FROM troughinfo WHERE troughid = $tid");

  if($result){
    if($result->num_rows <= 0){
      echo "<h1>trough id does not exists</h1>";
    }
    else {
      $result = $conn->query("DELETE FROM troughinfo WHERE troughid = $tid");
      if($result) {
        echo "<h1>Successfully removed troughid</h1>";
      }
      else {
        echo "<h1>Failed to delete trough id</h1></br>";
        echo $result;
      }
    }
  }
 ?>
