/***************************************************
==================== JS INDEX ======================
****************************************************

// Data Image Js
// Preloader Js
// Mobile Menu Overlay Js
// Mobile Menu Js
// Hamburger Menu Js
// Sticky Js
// Search Bar Js
// Cartmini Js
// Odometer Js
// Button hover animation Js
// Hero Slider Js
// Nice Select Js
// BeforeAfter Js
// Portfolio Slider Js
// Portfolio-2 Slider Js
// Portfolio-2 Active Js
// Testimonial Slider Js
// Testimonial-2 Slider Js
// Testimonial-3 Slider  Js
// Post-box Js
// Price Js
// Popup Js
// Video Js
// Portfolio filter Js
// Services Filter Js
// Backtotop Js
// Rating Js
// WOW Js

****************************************************/

(function ($) {
	"use strict";

	// Data Image Js
	$("[data-background").each(function () {
		$(this).css(
			"background-image",
			"url( " + $(this).attr("data-background") + "  )"
		);
	});

	// Preloader Js
	var windowOn = $(window);
	windowOn.on('load', function () {
		$(".loader-wrapper").fadeOut(500);
	});
	  
	// Mobile Menu Overlay Js
	var canva_expander = $(".canva_expander");
	if (canva_expander.length) {
		$(".canva_expander, #canva_close, #canvas-overlay-bg").on(
			"click",
			function (e) {
				e.preventDefault();
				$("body").toggleClass("canvas_expanded");
			}
		);
	}

	// Mobile Menu Js
	$(".main-mobile-menu").meanmenu({
		meanMenuContainer: ".mobile_menu",
		meanScreenWidth: "1199",
		meanExpand: ['<i class="fa-light fa-angle-right"></i>'],
	});
	$(".menu-bar").on("click", function () {
		$(".menu-bar").addClass("menu-bar-toggeled");
	});

	// Hamburger Menu Js
	$(".menu-bar").on("click", function () {
		$(".hamburger-area").addClass("opened");
		$(".body-overlay").addClass("opened");
	});
	$(".hamburger_close_btn").on("click", function () {
		$(".hamburger-area").removeClass("opened");
		$(".body-overlay").removeClass("opened");
		$(".menu-bar").removeClass("menu-bar-toggeled");
	});
	$(".body-overlay").on("click", function () {
		$(".hamburger-area").removeClass("opened");
		$(".body-overlay").removeClass("opened");
		$(".offset_canvas").removeClass("show");
		$(".menu-bar").removeClass("menu-bar-toggeled");
	});

	// Sticky Js
	$(window).scroll(function () {
		var Width = $(document).width();
		if ($("body").scrollTop() > 250 || $("html").scrollTop() > 250) {
			$(".header-sticky").addClass("sticky");
		} else {
			$(".header-sticky").removeClass("sticky");
		}
	});

	// Search Bar Js
	$(".tj-search-popup").on("click", function () {
		$(".search_popup").addClass("search-opened");
		$(".search-popup-overlay").addClass("search-popup-overlay-open");
	});
	$(".search_close_btn").on("click", function () {
		$(".search_popup").removeClass("search-opened");
		$(".search-popup-overlay").removeClass("search-popup-overlay-open");
	});
	$(".search-popup-overlay").on("click", function () {
		$(".search_popup").removeClass("search-opened");
		$(this).removeClass("search-popup-overlay-open");
	});

	// Cartmini Js
	$(".cartmini-open-btn").on("click", function () {
		$(".cartmini__area").addClass("cartmini-opened");
		$(".cartmini-overlay").addClass("openeds");
	});
	$(".cartmini-close-btn").on("click", function () {
		$(".cartmini__area").removeClass("cartmini-opened");
		$(".cartmini-overlay").removeClass("openeds");
	});
	$(".cartmini-overlay").on("click", function () {
		$(".cartmini__area").removeClass("cartmini-opened");
		$(".cartmini-overlay").removeClass("openeds");
	});

	// Odometer Js
	if ($(".odometer").length > 0) {
		$(".odometer").waypoint(
			function () {
				var odo = $(".odometer");
				odo.each(function () {
					var countNumber = $(this).attr("data-count");
					$(this).html(countNumber);
				});
			},
			{
				offset: "80%",
				triggerOnce: true,
			}
		);
	}

	// Button hover animation Js
	$(".tj-hover-btn").on("mouseenter", function (e) {
		var x = e.pageX - $(this).offset().left;
		var y = e.pageY - $(this).offset().top;
		$(this).find(".tj-hover-btn-circle-dot").css({
			top: y,
			left: x,
		});
	});
	$(".tj-hover-btn").on("mouseout", function (e) {
		var x = e.pageX - $(this).offset().left;
		var y = e.pageY - $(this).offset().top;
		$(this).find(".tj-hover-btn-circle-dot").css({
			top: y,
			left: x,
		});
	});

	// Hero Slider Js
	const sliderswiper = new Swiper(".tj-slider-2-active", {
		// Optional parameters
		speed: 1500,
		loop: true,
		slidesPerView: 1,
		autoplay: true,
		effect: "fade",
		breakpoints: {
			1600: {
				slidesPerView: 1,
			},
			1400: {
				slidesPerView: 1,
			},
			1200: {
				slidesPerView: 1,
			},
			992: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},

			a11y: false,
		},
		// Navigation arrows
		navigation: {
			nextEl: ".slider-next",
			prevEl: ".slider-prev",
		},
		pagination: {
			el: ".tj-portfolio-slide-dot",
			clickable: true,
			renderBullet: function (index, className) {
				return (
					'<span class="' +
					className +
					'">' +
					"<button>" +
					(index + 1) +
					"</button>" +
					"</span>"
				);
			},
		},
	});

	// Nice Select Js
	if ($("select").length > 0) {
		$("select").niceSelect();
	}

	// BeforeAfter Js
	if ($(".tj-before-after-wrapper").length > 0) {
		$(".tj-before-after-wrapper").beforeAfter({
			movable: true,
			clickMove: true,
			position: 50,
			separatorColor: "#fafafa",
			bulletColor: "#fafafa",
			onMoveStart: function (e) {
				console.log(event.target);
			},
			onMoving: function () {
				console.log(event.target);
			},
			onMoveEnd: function () {
				console.log(event.target);
			},
		});
	}

	// Portfolio Slider Js
	var slider = new Swiper(".tj-portfolio-active", {
		slidesPerView: 3,
		spaceBetween: 30,
		centeredSlides: true,
		loop: true,
		speed: 2000,
		autoplay: {
			delay: 5000,
		},
		breakpoints: {
			1200: {
				slidesPerView: 3,
			},
			992: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 1.5,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
		pagination: {
			el: ".tj-portfolio-slide-dot",
			clickable: true,
			renderBullet: function (index, className) {
				return (
					'<span class="' +
					className +
					'">' +
					"<button>" +
					(index + 1) +
					"</button>" +
					"</span>"
				);
			},
		},
	});

	// Testimonial Slider Js
	var slider = new Swiper(".tj-testimonial-active", {
		slidesPerView: 2,
		spaceBetween: 30,
		loop: true,
		speed: 2000,
		autoplay: {
			delay: 3000,
		},
		breakpoints: {
			1200: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 2,
			},
			768: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
		pagination: {
			el: ".tj-testimonial-slide-dot",
			clickable: true,
			renderBullet: function (index, className) {
				return (
					'<span class="' +
					className +
					'">' +
					"<button>" +
					(index + 1) +
					"</button>" +
					"</span>"
				);
			},
		},
	});

	// Portfolio-2 Slider Js
	var slider = new Swiper(".tj-portfolio-2-active", {
		slidesPerView: 5,
		spaceBetween: 30,
		centeredSlides: true,
		loop: true,
		speed: 2000,
		autoplay: {
			delay: 5000,
		},
		breakpoints: {
			1200: {
				slidesPerView: 5,
			},
			992: {
				slidesPerView: 3,
			},
			768: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			0: {
				slidesPerView: 1,
			},
		},
		pagination: {
			el: ".tj-portfolio-slide-dot",
			clickable: true,
			renderBullet: function (index, className) {
				return (
					'<span class="' +
					className +
					'">' +
					"<button>" +
					(index + 1) +
					"</button>" +
					"</span>"
				);
			},
		},
	});

	// Portfolio-2 Active Js
	$(".tj-portfolio-2-wrap").on("mouseenter", function () {
		$(this).addClass("active").siblings().removeClass("active");
	});
	
	// Testimonial-2 Slider Js
	var testimonialSwiper = new Swiper(".tj-testimonial-2-active", {
		slidesPerView: 1,
		spaceBetween: 35,
		loop: true,
		speed: 1500,
		navigation: {
			nextEl: ".slider-next",
			prevEl: ".slider-prev",
		},
	});
	testimonialSwiper.on("slideChange", function () {
		var nxSlide = $(".tj-testimonial-2-active .swiper-wrapper")
			.children()
			.eq(testimonialSwiper.realIndex + 1)
			.next();
		var pvSlide = $(".tj-testimonial-2-active .swiper-wrapper")
			.children()
			.eq(testimonialSwiper.realIndex + 1)
			.prev();

		$(".slider-next img").fadeOut("slow", function () {
			$(this).animate({ opacity: 0 }, 100);
			$(this).attr("src", nxSlide.find("img").attr("data-src"));
			$(this).fadeIn("slow", function () {
				$(this).animate({ opacity: 1 }, 100);
			});
		});

		$(".slider-prev img").fadeOut("slow", function () {
			$(this).animate({ opacity: 0 }, 100);
			$(this).attr("src", pvSlide.find("img").attr("data-src"));
			$(this).fadeIn("slow", function () {
				$(this).animate({ opacity: 1 }, 100);
			});
		});
	});

	// Testimonial-3 Slider  Js
	var slider = new Swiper(".tj-testimonial-3-active", {
		direction: "vertical",
		slidesPerView: 3,
		spaceBetween: 30,
		centeredSlides: true,
		loop: true,
		speed: 1500,
		// autoplay: {
		// 	delay: 2000,
		// },
		// Navigation arrows
		navigation: {
			nextEl: ".slider-next",
			prevEl: ".slider-prev",
		},
	});

	// Post-box Js
	var slider = new Swiper(".tj-post-item-slide-active", {
		slidesPerView: 1,
		centeredSlides: true,
		spaceBetween: 30,
		loop: true,
		speed: 2000,
		// Navigation arrows
		navigation: {
			nextEl: ".swiper-button-next",
			prevEl: ".swiper-button-prev",
		},
	});

	// Price Js
	var price = $(".price-number");
	var year = $("#year");
	var month = $("#month");
	year.on("click", function () {
		$(this).addClass("active");
		month.removeClass("active");
		price.each(function () {
			$(this).text($(this).data("year-price"));
		});
	});
	month.on("click", function () {
		$(this).addClass("active");
		year.removeClass("active");
		price.each(function () {
			$(this).text($(this).data("month-price"));
		});
	});

	// Popup Js
	$(document).ready(function () {
		$(".popup-gallery").magnificPopup({
			delegate: "a",
			type: "image",
			mainClass: "mfp-fade",
			gallery: {
				enabled: true,
			},
		});
	});

	// Video Js
	var popupvideos = $(".popup-videos-button");
	if (popupvideos.length) {
		$(".popup-videos-button").magnificPopup({
			disableOn: 10,
			type: "iframe",
			mainClass: "mfp-fade",
			removalDelay: 160,
			preloader: false,
			fixedContentPos: false,
		});
	}

	// Portfolio filter Js
	$("#portfolio-grid").isotope({
		itemSelector: ".finance",
		percentPosition: true,
		masonry: {
			// use outer width of grid-sizer for columnWidth
			columnWidth: ".grid-sizer",
		},
	});
	$("#portfolio-grid").imagesLoaded(function () {
		$(".filter-menu").on("click", "button", function () {
			var filterValue = $(this).attr("data-filter");
			$grid.isotope({
				filter: filterValue,
			});
		});
		$(".filter-menu button").on("click", function (event) {
			$(this).siblings(".active").removeClass("active");
			$(this).addClass("active");
			event.preventDefault();
		});
		var $grid = $("#portfolio-grid").isotope({
			itemSelector: ".tj-portfolio-3-wrapper",
			percentPosition: true,
			masonry: {
				columnWidth: ".tj-portfolio-3-wrapper",
			},
		});
	});

	// Services Filter Js
	$(".service-filter-btn").click(function () {
		$(".service-filter-btn").removeClass("active");
		$(".tab-item-widget div").removeClass("active");

		$(this).addClass("active");
		$("." + $(this).attr("id")).addClass("active");
	});

	// Backtotop Js
	function back_to_top() {
		var btn = $("#back_to_top");
		var btn_wrapper = $(".back-to-top-wrapper");

		$(window).scroll(function () {
			if ($(window).scrollTop() > 300) {
				btn_wrapper.addClass("back-to-top-btn-show");
			} else {
				btn_wrapper.removeClass("back-to-top-btn-show");
			}
		});

		btn.on("click", function (e) {
			e.preventDefault();
			$("html, body").animate({ scrollTop: 0 }, "300");
		});
	}
	back_to_top();

	// Rating Js
	if ($(".fill-ratings span").length > 0) {
		var star_rating_width = $(".fill-ratings span").width();
		$(".star-ratings").width(star_rating_width);
	}

	// WOW Js
	$(window).on("load", function () {
		var wow = new WOW({
			boxClass: "wow", // default
			animateClass: "animated", // default
			offset: 0, // default
			mobile: true, // default
			live: true, // default
		});
		wow.init();
	});

})(jQuery);
