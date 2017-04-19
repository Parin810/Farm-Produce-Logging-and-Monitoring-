<?php
class ControllerCustomCustomtask extends Controller {
	public function index() {
		$this->load->language('common/dashboard');
		$this->document->setTitle("Custom Task");

		$data['heading_title'] = "Custom Tasks";
    $data['hello'] = "Hello";
		// Check install directory exists
		if (is_dir(dirname(DIR_APPLICATION) . '/install')) {
			$data['error_install'] = $this->language->get('error_install');
		} else {
			$data['error_install'] = '';
		}

		$data['token'] = $this->session->data['token'];

		$data['header'] = $this->load->controller('common/header');
		$data['column_left'] = $this->load->controller('common/column_left');
		$data['footer'] = $this->load->controller('common/footer');

		$this->response->setOutput($this->load->view('custom/customtask', $data));
	}
}
