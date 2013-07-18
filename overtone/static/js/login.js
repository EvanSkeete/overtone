$(function(){

var dom = {};
var ui = {};

var _dom = function(){
	dom.login_box = $('.login-box');
	dom.login_form = $('.login-form');
	dom.sign_up = $('.sign_up');
	dom.confirm_password = $('input[name="confirm_password"]');
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
};

var _init = function(){
	_dom();
	_ui();
	_bindings();
};

_init();

});