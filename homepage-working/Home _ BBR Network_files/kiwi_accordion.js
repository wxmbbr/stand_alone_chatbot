jQuery(function($) {
    // Falls die Konstante nicht gesetzt wurde...
    if(typeof tx_kiwiaccordion_effect == 'undefined') {
        tx_kiwiaccordion_effect = 'none';
    }
    // Elemente vorbereiten
    $('.ka-panel').each(function() {
        //Erste Überschrift suchen
        $header = $(':header:first', this);     
        //Fehler Behandlung wenn keine Überschrift vorhanden ist
        if($header.length == 0) {
            $(this).addClass('ka-error').removeClass('ka-panel');
            console.error('This panel contains no header.', this);
        }
        else {
            //kleiner trick um <div class="csc-header"><h1>... abzufangen           
            if($header.parent().find('*').length == 1 && !$header.parent().is('.ka-panel')) {
                $header.parent().addClass('ka-handler');
            }
            else {
                $header.addClass('ka-handler');
            }
            
            //Inhalte umschließen für die Ansprache
            $('.ka-handler', this).nextAll().wrapAll('<div class="ka-content"></div>');
            
            //prüfen ob ein Fehler aufgetreten ist
            if($('.ka-content .ka-handler', this).length > 0) {
                console.error('Handler may not be wrapped by more then one element.', this);
                $(this).addClass('ka-error').removeClass('ka-panel');
            }
        }
    });
    // Versteckte Inhalte nicht anzeigen
    $('.ka-panel.accordionClose .ka-content').hide();
    // Für ein paar Effekte
    $('.ka-panel .ka-handler').hover(function() {
        $(this).parents('.ka-panel').addClass('hover');
    }, function() {
        $(this).parents('.ka-panel').removeClass('hover');
    });
    // Eventhandler
    $('.ka-handler').click(function(event, data) {
        $panel = $(this).parents('.ka-panel');
        $content = $panel.find('.ka-content');      
        if($panel.is('.accordionClose')) {
            $('.ka-panel.ka-opend').removeClass('ka-opend');
            //Dieses Panel aufklappen
            //console.log(tx_kiwiaccordion_effect);
            switch(tx_kiwiaccordion_effect) {
                case 'slide':
                    $content.slideDown();
                    break;
                case 'fade':
                    $content.fadeIn();
                    break;
                default:
                    $content.show();                
            }
            $panel.removeClass('accordionClose').addClass('accordionOpen');
            //Wenn nur ein offenes Panel erlaubt ist, andere Panels schließen
            if(tx_kiwiaccordion_exclusive) {
                $('.ka-panel.accordionOpen .ka-handler').trigger('click', {clicked: $('.ka-panel').index($panel)});
            }
        }
        else {
            if(!data) {
                data = { clicked: -1 };
            }
            if(data.clicked != $('.ka-panel').index($panel)) {
                //Diesen Panel zuklappen
            //console.log(tx_kiwiaccordion_effect);
                switch(tx_kiwiaccordion_effect) {
                    case 'slide':
                        $content.slideUp();
                        break;
                    case 'fade':
                        $content.fadeOut();
                        break;
                    default:
                        $content.hide();                
                }
                $panel.removeClass('accordionOpen').addClass('accordionClose');
            }
        }
    }); 
});