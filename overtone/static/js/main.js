//Globals
var player;
dom = {};
ajax = {};
handlers = {};
ui={};


var _dom = function(){
    dom.search_bar = $('.search-bar');
    dom.overlay = $('.overlay');
    dom.search_container = $('.search-container');
    dom.library_body = $('.library-body');
    dom.loading_screen = $('.loading-screen');
};

var _data = function(){

};

var _ajax = function(){
    ajax.add_song = function(song){
        $.ajax({
              type: "POST",
              url: "/add_song",
              data: { name: song.name , videoId: song.videoId, artist: song.artist }
        });
    };

    ajax.modify_song = function(values){
        $.ajax({
              type: "POST",
              url: "/modify_song",
              data: values
        });
    };

    ajax.search = function(search){
        var request = gapi.client.youtube.search.list({
            'part':'snippet',
            'q':search,
            'maxResults':20,
            'videoCategoryId':'10',
            'type':'video'
        });

        var results = [];

        request.execute(function(response){
            $.each(response.items, function(index, item){
                results.push({'videoId': item.id.videoId, 'title': item.snippet.title, 'thumbs':item.snippet.thumbnails});
                console.log(item.snippet);
            });
            ui.render_search_results(results);
        });
    };
};

var _ui = function(){
    ui.render_search_results = function(results){
    dom.search_container.html('');
    dom.search_container.append('<h3><strong>Click to play, or drag into library</strong></h3>');
    $.each(results, function(index,result){
        var result_dom = $('<p>'+result.title+'</p>');
        var thumb = $('<div class="thumb"><img src="'+result.thumbs.medium.url+'"></img></div>');
        result_dom.append(thumb);
        result_dom.data('title',result.title);
        result_dom.data('videoId',result.videoId);
        dom.search_container.append(result_dom);
    });
};

};

var _handlers = function(){

};

var _bindings = function(){
        dom.search_bar.on('focus', function(){
        dom.search_bar.val('');
        dom.overlay.fadeIn(300);
    });

    dom.search_container.on('click','p', function(event){
        var result = $(event.target).parents('p');
        var split_title = result.data('title').split('-');
        var videoId = result.data('videoId');

        var name, artist = '';
        var name_string, artist_string = '';

        if(split_title.length > 1){
            name_string = split_title[1];
            artist_string = split_title[0];
            name = $('<td>' + name_string + '</td>');
            artist = $('<td>' + artist_string + '</td>');

        }else{
            name_string = split_title[0];
            artist_string = '';
            name = $('<td>' + name_string + '</td>');
            artist = $('<td></td>');
        }

        log.debug(result, "Clicked on:");

        var tr = $('<tr>');
        name.addClass('name');
        artist.addClass('artist');
        var number = $('<td></td>').addClass('number');
        var album = $('<td></td>').addClass('album');
        var time = $('<td></td>').addClass('time');
        var plays = $('<td>1</td>').addClass('plays');

        tr.append(number, name, artist, album, time, plays);
        tr.data('videoId',videoId);
        dom.library_body.append(tr);

        player.loadVideoById(videoId, 0, 'large');
        ajax.add_song({'name':name_string, 'artist':artist_string, 'videoId':videoId});
        dom.overlay.fadeOut(300);
    });

    dom.overlay.click(function(event){
        dom.overlay.fadeOut(300);
    });

    dom.library_body.on('click','tr', function(event){
        var result = $(event.target).parents('tr');
        var videoId = result.data('videoId');
        player.loadVideoById(videoId, 0, 'large');
        //Increase play count
        var plays = parseInt(result.find('.plays').html(),10);
        plays += 1;
        result.find('.plays').html(plays);
        ajax.modify_song({'videoId':videoId,'plays':plays});
    });


    $(document).on('keyup', function(event){
        if(event.keyCode == 27){
            dom.overlay.fadeOut(300);
        }else{
            //player.loadVideoById("bHQqvYy5KYo");
        }
    });

    dom.search_bar.on('keyup', function(event){
        if(event.keyCode == 13){
            ajax.search(dom.search_bar.val());
        }
    });
};

$(function(){
    log.info("Document Loaded");
    _dom();
    _ajax();
    _ui();
});

var init = function(){

    _handlers();
    _bindings();

    log.info("Initalized");
    dom.loading_screen.hide();

    //Load the first song
    videoId = dom.library_body.find('tr').first().data('videoId');
    player.loadVideoById(videoId, 0, 'large');
};

YoutubeLoad = $.Deferred();
PlayerReady = $.Deferred();

$.when(YoutubeLoad, PlayerReady).done(init);

OnYoutubeLoad = function(){
    gapi.client.setApiKey('AIzaSyDyzJiYzti6AgGrCeguYAgPC-zPuDeRDqY');
    gapi.client.load('youtube', 'v3', function(){
        log.info("Api Loaded");
        YoutubeLoad.resolve();
    });
};

var onYouTubeIframeAPIReady = function(){
    log.info('Player Ready');

    player = new YT.Player('player', {
      height: '315',
      width: '560',
      videoId: ''
    });
    PlayerReady.resolve();
};

var onPlayerStateChange = function(event) {
    log.info(event, "Player State Change");
};

var log = (function(){

    infoOn = true;
    debugOn = false;

    return{
        info: function(data, event){
            if(this.infoOn){
                event = typeof event == "undefined" ? "" : event;
                console.log('------------------------ INFO: '+event+' ------------------------');
                console.log(data);
            }
        },

        debug: function(data, event){
            if(this.debugOn){
                event = typeof event == "undefined" ? "" : event;
                console.log('------------------------ DEBUG: '+event+'------------------------');
                console.log(data);
            }
        },

        setStatus : function(status){
            this.infoOn = status.info;
            this.debugOn = status.debug;
        }
    };
})();

log.setStatus({info:true, debug:true});
