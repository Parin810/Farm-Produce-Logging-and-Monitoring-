
<!-- Custom Fonts -->
<link href="../admin/view/javascript/datepicker/css/bootstrap-datepicker3.min.css" rel="stylesheet" type="text/css">

<?php echo $header; ?><?php echo $column_left; ?>
<div id="content">
  <div class="page-header">
    <div class="container-fluid">
      <h1><?php echo $heading_title; ?></h1>
    </div>
  </div>
  <div class="container-fluid">
    <?php if ($error_install) { ?>
    <div class="alert alert-danger"><i class="fa fa-exclamation-circle"></i> <?php echo $error_install; ?>
      <button type="button" class="close" data-dismiss="alert">&times;</button>
    </div>
    <?php } ?>
    <div class="row">
      <!-- export csv -->
      <div class="col-md-6">
       <h3>Export CSV File</h3>
        <form action="custom/processcsv.php" method="post">
          <div>
            <div>
              <div class="form-group">
                  <label>Start date:</label>
                  <input class="form-control datepickerbox" type="text" name="startdate">
              </div>
            </div>
          </div>

          <div>
            <div>
              <div class="form-group">
                  <label>End date:</label>
                  <input class="form-control datepickerbox" type="text" name="enddate">
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-default">Export</button>
        </form>
      </div>

      <!-- add or remove troughid -->
      <div class="col-md-6">
       <h3>Add New Trough ID</h3>
        <form action="custom/addtroughid.php" method="post">
          <div>
            <div>
              <div class="form-group">
                  <label>Enter new trough ID:</label>
                  <input class="form-control" type="number" name="addtroughid">
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-default">Add</button>
        </form>
        <br/>
        <h3>Remove Trough ID</h3>
         <form action="custom/rmtroughid.php" method="post">
           <div>
             <div>
               <div class="form-group">
                   <label>Enter trough ID:</label>
                   <input class="form-control" type="number" name="rmtroughid">
               </div>
             </div>
           </div>
           <button type="submit" class="btn btn-default">Remove</button>
         </form>
      </div>
    </div>
    <div class="row" style="margin-top:20px;">
      <!-- add or remove location -->
      <div class="col-md-6">
       <h3>Add New Location</h3>
        <form action="custom/addlocation.php" method="post">
          <div>
            <div>
              <div class="form-group">
                  <label>Enter new location:</label>
                  <input class="form-control" type="text" name="addlocation">
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-default">Add</button>
        </form>
        <br/>
        <h3>Remove Location</h3>
         <form action="custom/rmlocation.php" method="post">
           <div>
             <div>
               <div class="form-group">
                   <label>Enter location:</label>
                   <input class="form-control" type="text" name="rmlocation">
               </div>
             </div>
           </div>
           <button type="submit" class="btn btn-default">Remove</button>
         </form>
      </div>
      <div class="col-md-6">
        <h3>Show Info</h3>
        <form action="custom/showtroughid.php" method="post">
          <button type="submit" class="btn btn-default">Show Trough IDs</button>
        </form>
        <br>
        <form action="custom/showlocation.php" method="post">
          <button type="submit" class="btn btn-default">Show locations</button>
        </form>
      </div>
    </div>
  </div>
</div>
<!-- jQuery -->
<script src="../admin/view/javascript/jquery/jquery-2.1.1.min.js"></script>
<!-- Flot Charts JavaScript -->
<script language="javascript" type="text/javascript" src="../admin/view/javascript/flot/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="../admin/view/javascript/flot/jquery.flot.categories.js"></script>
<script src="../admin/view/javascript/datepicker/js/bootstrap-datepicker.min.js"></script>

<script type="text/javascript">
    $('.datepickerbox').datepicker({
    format: "yyyy-mm-dd"
  });
</script>

<?php echo $footer; ?>
