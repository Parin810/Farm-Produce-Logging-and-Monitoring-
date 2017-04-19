<?php

  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }
 $result = $conn->query("SELECT name, quantity FROM oc_product_description INNER JOIN oc_product ON oc_product.product_id = oc_product_description.product_id");
   while($row = $result->fetch_assoc()){
     $dataset[] = array( $row['name'], $row['quantity'] );
   }
 ?>
<?php echo $header; ?><?php echo $column_left; ?>
<div id="content">
  <div class="page-header">
    <div class="container-fluid">
      <h1><?php echo $heading_title; ?></h1>
      <ul class="breadcrumb">
        <?php foreach ($breadcrumbs as $breadcrumb) { ?>
        <li><a href="<?php echo $breadcrumb['href']; ?>"><?php echo $breadcrumb['text']; ?></a></li>
        <?php } ?>
      </ul>
    </div>
  </div>
  <div class="container-fluid">
    <?php if ($error_install) { ?>
    <div class="alert alert-danger"><i class="fa fa-exclamation-circle"></i> <?php echo $error_install; ?>
      <button type="button" class="close" data-dismiss="alert">&times;</button>
    </div>
    <?php } ?>
    <div class="row">
      <div class="col-lg-3 col-md-3 col-sm-6"><?php echo $order; ?></div>
      <div class="col-lg-3 col-md-3 col-sm-6"><?php echo $sale; ?></div>
      <div class="col-lg-3 col-md-3 col-sm-6"><?php echo $customer; ?></div>
      <div class="col-lg-3 col-md-3 col-sm-6"><?php echo $online; ?></div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-md-12 col-sx-12 col-sm-12"><?php echo $chart; ?></div>
    </div>
    <div class="row">
      <div class="col-lg-12 col-md-12 col-sx-12 col-sm-12">
        <div class="panel panel-default">
          <div class="panel-heading">
            <h3 class="panel-title"><i class="fa fa-bar-chart-o"></i>Stock Status</h3>
          </div>
          <div class="panel-body">
            <div id="chart-stock" style="width: 100%; height: 260px;"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-4 col-md-12 col-sm-12 col-sx-12"><?php echo $activity; ?></div>
      <div class="col-lg-8 col-md-12 col-sm-12 col-sx-12"> <?php echo $recent; ?> </div>
    </div>
  </div>
</div>
<!-- jQuery -->
<script src="../admin/view/javascript/jquery/jquery-2.1.1.min.js"></script>
<!-- Flot Charts JavaScript -->
<script language="javascript" type="text/javascript" src="../admin/view/javascript/flot/jquery.flot.js"></script>
<script language="javascript" type="text/javascript" src="../admin/view/javascript/flot/jquery.flot.categories.js"></script>

<script type="text/javascript">
var dataset = <?php echo json_encode($dataset); ?>;

var option = {
  shadowSize: 0,
  colors: ['#9FD5F1', '#1065D2'],
  bars: {
    show: true,
    fill: true,
    lineWidth: 1
  },
  grid: {
    backgroundColor: '#FFFFFF',
    hoverable: true
  },
  points: {
    show: false
  },
  xaxis: {
    show: true,
          ticks: 0
  }
}

  $.plot("#chart-stock", [ {data:dataset, color:'blue'} ], {
    series: {
      bars: {
        show: true,
        align: "center",
        barWidth: 0.4
      }
    },
    xaxis: {
      mode: "categories",
      tickLength: 0
    }
  }, option);

</script>

<?php echo $footer; ?>
