<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $result = $conn->query("SELECT * FROM locationinfo");

  if($result){
    if($result->num_rows > 0){
      echo "<h1>Location Info</h1></br>";
      while($row = $result->fetch_assoc()){
        echo $row['locationid'].' '.$row['locationname'].'</br>';
      }
    }
    else {
      echo "There are no locations";
    }
  }
  else {
    echo "<h1>Failed to display LocationInfo</h1>";
    echo $result;
  }
 ?>
