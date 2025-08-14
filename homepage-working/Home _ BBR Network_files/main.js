
// Videoplayer Slider
jQuery(window).resize(function() {
    resizeYTPlayer();
});

function resizeYTPlayer() {
	if (jQuery('.slider-video .player').length > 0) {
		setTimeout(function() {
			currentWidth = parseInt(jQuery('.slider-video').width());
			currentHeight = parseInt(jQuery('.slider-video').height());

			mod = 1.7777777777777777777777777777778;
			minVideoWidth = parseInt(650*mod);
			minVideoHeight = 650;
			
			if (currentWidth < minVideoWidth) {
				jQuery('.player').width(minVideoWidth+'px');
				jQuery('.player').css('max-width','unset');
				
				videoMarginWidth = '-'+parseInt((minVideoWidth-currentWidth)/2)+'px';
				jQuery('.player').css('margin-left',videoMarginWidth);
				jQuery('.player').css('margin-top','unset');
			} else {
				jQuery('.player').width(currentWidth+'px');
				jQuery('.player').height(parseInt(currentWidth/mod)+'px');
				
				videoMarginHeight = '-'+(parseInt((jQuery('.player').height()-minVideoHeight)/2))+'px';
				jQuery('.player').css('margin-top',videoMarginHeight);
				jQuery('.player').css('margin-left','unset');
			}
		},5000);
	} 
}



jQuery(document).ready(function() {
	resizeYTPlayer();
	/* for focuspoint use
	jQuery('.focusPending').each(function() {
		jQuery(this).attr('data-focus-x',(jQuery(this).data('ofocus-x')+0.05)*2-1);
		jQuery(this).attr('data-focus-y',(jQuery(this).data('ofocus-y')+0.05)*-2+1);
		jQuery(this).attr('data-image-w',jQuery(this).children('img').width());
		jQuery(this).attr('data-image-h',jQuery(this).children('img').height());
		jQuery(this).toggleClass('focusPending focuspoint');
	});
	jQuery('.focuspoint').focusPoint();
	*/
	if (jQuery('.footable').length > 0) {
		jQuery('.footable').footable();
	}
	if (jQuery('.datepicker').length > 0) {
		jQuery('.datepicker').datepicker();
	}
	jQuery("#mobileNavi").mmenu({
		classes: "mm-zoom-panels",
		counters: true,
		footer: {
			add: true,
			title: jQuery('#mobileNaviLang').html()+jQuery('#mobileNaviPhone').html()
		},
		searchfield: {
			placeholder: "Menü durchsuchen ...",
			noResults: "Keine entsprechende Seite gefunden",
			add: false,
			search: false
		}
	});
    
    //BOOTSTRAP MENU MIT HOVER
    jQuery('.dropdown-toggle').click(function() { var location = $(this).attr('href'); window.location.href = location; return false; });
    
	jQuery("#mobileNaviTriggerWrap").click(function(e) {
		e.preventDefault();
		jQuery("#mobileNavi").trigger("open.mm");
	});
	jQuery('.mm-subopen').html('<i class="fas fa-angle-right"></i>');
	jQuery('.mm-subclose').prepend('<i class="fas fa-angle-left"></i>');
	addToHomescreen();
});


/* news slider */

jQuery('#mainpage .news-list-view').slick({
	arrows: true,
  	autoplay: false,
  	dots: false,
  	slidesToShow: 3,
    responsive: [
				{
   				breakpoint: 1025,
      			settings: {
        			slidesToShow: 2,
        			slidesToScroll: 1
     				}
    		},
    			{
   				breakpoint: 430,
      			settings: {
        			slidesToShow: 1,
        			slidesToScroll: 1
     				}
    			}
  			]			
});


// mobile navi


$('li.top-level.dropdown > a, li.top-level.dropdown > span').click(function(e){
	e.preventDefault();
    if($(this).parent().hasClass('open')){
		$(this).parent().removeClass('open')
	}else{
	$(this).parent().addClass('open')
	}
});


$('li.dropdown-level .open-icon').click(function(e){
    if($(this).parent().hasClass('open')){
		$(this).parent().removeClass('open')
	}else{
	$(this).parent().addClass('open')
	}
});

$('#mobileNaviTriggerWrap').click(function(e){
	e.preventDefault();
	$('.wrapAll').toggleClass('show-menu');
});



	/*suche*/
	
	$('.lupe').click(function() {
		jQuery('.navi-search').toggleClass('opened');
	});


// list style

jQuery('#main li').each(function (){
	jQuery(this).prepend('<i class="fas fa-chevron-right"></i>');
	
});


/*
var resizeTimer;
jQuery(window).resize(function() {
    randomFunction();
    resizeTimer = setTimeout(randomFunction, 300);	
}); 
*/

/* Random Slickslider */
jQuery.fn.randomize = function(selector) {
	var $elems = selector ? $(this).find(selector) : $(this).children(), $parents = $elems.parent();
	$parents.each(function() {
		$(this).children(selector).sort( function(childA, childB) {
			return Math.round(Math.random()) - 0.5;
		}.bind(this)).detach().appendTo(this);
	});
	return this;
};