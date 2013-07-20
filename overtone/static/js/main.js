$(function(){
var dom = {};
var ui = {};
var ajax = {};

var _dom = function(){
	dom.login_box = $('.main-box');
	dom.entry_form = $('.entry-form');
	dom.playlist_form = $('.playlist-form');
	dom.list = $('.list');
	dom.playlist_list = $('.playlist-list');
};


var _ajax = function(){
	ajax.add_entry = function(event){
	event.preventDefault();
	$.ajax({
		type: 'post',
		url: '/add_entry',
		data: dom.entry_form.serialize(), // serializes the form's elements.
		success: function(result)
		{
			if(result.status){
				ui.add_entry(result.data);
				console.log(result.status);
			}
		}
	});
	return false;
	};

	ajax.add_playlist = function(event){
	event.preventDefault();
	$.ajax({
		type: 'post',
		url: '/add_playlist',
		data: dom.playlist_form.serialize(), // serializes the form's elements.
		success: function(result)
		{
			console.log('callback');
			if(result.status){
				ui.add_playlist(result.name);
				console.log(result.name);
			}
		}
	});
	return false;
	};
};


var _ui = function(){
	ui.add_entry = function(data){
		dom.list.append('<li>'+data+'</li>');
	};

	ui.add_playlist = function(name){
		dom.playlist_list.append('<li>'+name+'</li>');
	};
};

var _bindings = function(){
	dom.entry_form.submit(ajax.add_entry);
	dom.playlist_form.submit(ajax.add_playlist);
};

var _init = function(){
	_dom();
	_ajax();
	_ui();
	_bindings();
};

_init();

});