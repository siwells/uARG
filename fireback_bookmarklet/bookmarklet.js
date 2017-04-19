

(function() {
    var zMax = 50000;
    function nextZ()        { return zMax++; }
    if (window.__MODAL__)   { window.__MODAL__.remove(); }
    
      b=document.getElementsByTagName('body')[0];
      otherlib=false;
     
      if(typeof jQuery!='undefined') 
      {
        console.log('This page already using jQuery v'+jQuery.fn.jquery);
        return doStuff();
      } else if (typeof $=='function') 
      {
        otherlib=true;
      }
     
      function getScript(url,success)
      {
        var script=document.createElement('script');
        script.src=url;
        var head=document.getElementsByTagName('head')[0],
            done=false;
        script.onload=script.onreadystatechange = function(){
          if ( !done && (!this.readyState
               || this.readyState == 'loaded'
               || this.readyState == 'complete') ) {
            done=true;
            success();
            script.onload = script.onreadystatechange = null;
            head.removeChild(script);
          }
        };
        head.appendChild(script);
      }
      
      getScript('http://code.jquery.com/jquery.min.js', function() {
        if (typeof jQuery=='undefined') {
          console.log('Sorry, but jQuery wasn\'t able to load');
        } else {
            console.log('This page is now jQuerified with v' + jQuery.fn.jquery);
                              
          if (otherlib) {msg+=' and noConflict(). Use $jq(), not $().';}
          
          console.log(jQuery.fn.jquery);
        }
        return doStuff();
      });
      
      function doStuff(){
        $(document).ready(function() {
        
            var location = document.location;
            var title = document.title;
            var selected = getSelectedText();

            if (selected) {

                var KEYCODE_ESC = 27;
                var $iframe = $('<iframe />')
                    .attr('id','my_iframe')
                    .attr('src','http://localhost:8910/test_iframe/remote.html?quote='+selected+'&url='+location+'&title='+title+'&rnd='+Math.floor(Math.random()*10000))
                    .attr('name','argublog')
                    .attr('ALLOWTRANSPARENCY','true')
                    .attr('frameborder','0')
                    .attr('width','90%')
                    .attr('height','90%')
                    .css('top', '25px')
                    .css('position', 'fixed')
                    .css('z-index', '999999999')
                    .css('overflow', 'auto');
                
                $('body').append($iframe);
                
                $iframe.hide().fadeIn("slow");                                
            }
            else
                alert('Please select some text to quote in your response.');
         });
      }
      
      function getSelectedText() {
            var SelText = '';
            if (window.getSelection) {
                SelText = window.getSelection().toString();
            } else if (document.getSelection) {
                SelText = document.getSelection().toString();
            } else if (document.selection) {
                SelText = document.selection.createRange().text;
            }
            return SelText;
        };
    
    })();

