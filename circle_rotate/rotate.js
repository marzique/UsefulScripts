// rotate circles relative to mouse position

var big = $(".big");
var offset_big = big.offset();
var width_big = big.outerWidth();
var height_big = big.outerHeight();
var centerX_big = offset_big.left + width_big / 2;
var centerY_big = offset_big.top + height_big / 2;

var small = $(".small");
var offset_small = big.offset();
var width_small = big.outerWidth();
var height_small = big.outerHeight();
var centerX_small = offset_small.left + width_small / 2;
var centerY_small = offset_small.top + height_small / 2;

$('#slider').mousemove(function(event) {
    if ( (!$("#title_main").hasClass("opened")) && !isMobile ){
        var angle_big = Math.atan2(event.pageY - centerY_big, event.pageX - centerX_big) * 180 / Math.PI;
        var angle_small = Math.atan2(event.pageY - centerY_small, event.pageX - centerX_small) * 180 / Math.PI;

        var angle_big_full = angle_big <= 0 ? angle_big : -180 - (180 - angle_big);
        var angle_small_full = angle_small <= 0 ? angle_small : -180 - (180 - angle_small);

        $(".big").css({"-webkit-transform":"rotate(" + angle_big_full + "deg)"});
        $(".small").css({"-webkit-transform":"rotate(" + angle_small_full + "deg)"});
    }
});
