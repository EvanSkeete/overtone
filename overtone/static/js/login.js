
$(function(){
var dom = {};
var ui = {};
var ajax = {};

var _dom = function(){
	dom.login_box = $('.login-box');
	dom.login_form = $('.login-form');
	dom.sign_up = $('.sign_up');
	dom.confirm_password = $('input[name="confirm_password"]');
};

var _ajax = function(){
	ajax.submit_login = function(event){
		//event.preventDefault();
		$.ajax({
			type: dom.login_form.attr('method'),
			url: dom.login_form.attr('action'),
			data: dom.login_form.serialize(), // serializes the form's elements.
			success: function(result)
			{
				if(result.status){
					window.location = '/main';
				}else{
					console.log(result.status);
				}
			}
		});
		return false;
	};

};

var _ui = function(){
	ui.display_register = function(){
		dom.login_form.attr('action', '/register');
		dom.login_box.css({'min-height':'500px'});
		dom.confirm_password.show('200');
	};
};

var _bindings = function(){
	dom.sign_up.on('click', ui.display_register);
	dom.login_form.submit(ajax.submit_login);
};

var _init = function(){
	_dom();
	_ajax();
	_ui();
	_bindings();
};

_init();

});