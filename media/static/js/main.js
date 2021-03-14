$(document).ready(()=>{
    
    var top = $("#contenido").position().top
    console.log(window.location.href.indexOf('metodos_probabilisticos'));    
    if(window.location.href.indexOf('metodos_probabilisticos') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }
    console.log(window.location.href.indexOf('metodos_randoms'));
    if(window.location.href.indexOf('metodos_randoms') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }

    if(window.location.href.indexOf('metodos_regresion') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }

    if(window.location.href.indexOf('metodos_simulacion') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }

    if(window.location.href.indexOf('modelo_real') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }

    if(window.location.href.indexOf('modelos_simulacion') > -1){   
        $('html, body').animate({
            scrollTop:top
        },800);        
    }
});