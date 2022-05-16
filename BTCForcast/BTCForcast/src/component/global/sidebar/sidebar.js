import React,{useEffect} from "react";
import { BrowserRouter, BrowserRouter as Router,Route,Switch } from "react-router-dom";
import ReactDOM from 'react-dom';


import { NavLink,Link } from "react-router-dom";
import $ from 'jquery';

import drivers from "../../../images/drivers.svg";
import financial from "../../../images/financial.svg";
import home from "../../../images/home.svg";
import load from "../../../images/load.svg";
import map from "../../../images/map.svg";
import setting from "../../../images/setting.svg";
import profile from "../../../images/profile.jpg";
import BTC_logo from "../../../images/BTC_logo.svg";
import dashboardIco from "../../../images/dashboardIco.svg";
import cryptoIco from "../../../images/cryptoIco.svg";
import publicIco from "../../../images/publicIco.svg";


function Sidebar() {

  useEffect(()=>{
    sidebarFunctionality()
  })

    const sidebarFunctionality=()=>{
      /* eslint-disable */
        "use strict";
        $("#sidebarToggle, #sidebarToggleTop").on("click", function (e) {
            $("body").toggleClass("sidebar-toggled"), $(".sidebar").toggleClass("toggled"), $(".sidebar").hasClass("toggled") && $(".sidebar .collapse").collapse("hide");
        }),
        $(window).resize(function () {
          $(window).width() < 768 && $(".sidebar .collapse").collapse("hide"),
          $(window).width() < 480 && !$(".sidebar").hasClass("toggled") && ($("body").addClass("sidebar-toggled"), $(".sidebar").addClass("toggled"), $(".sidebar .collapse").collapse("hide"));
            }),
            $("body.fixed-nav .sidebar").on("mousewheel DOMMouseScroll wheel", function (e) {
                var o;
                768 < $(window).width() && ((o = (o = e.originalEvent).wheelDelta || -o.detail), (this.scrollTop += 30 * (o < 0 ? 1 : -1)), e.preventDefault());
            }),
            $(document).on("scroll", function () {
                100 < $(this).scrollTop() ? $(".scroll-to-top").fadeIn() : $(".scroll-to-top").fadeOut();
            });
           
    }
      

    return(
        <>

             {/* Sidebar */}
          <ul className="navbar-nav sidebar sidebar-dark accordion zi-1 pb-100" id="accordionSidebar">
            {/* Sidebar - Brand */}
            <Link className="sidebar-brand d-flex align-items-center justify-content-center mt-2" to="/">
             
              <div className="sidebar-brand-text ">
                <img src={BTC_logo} className="" alt="apollo" />
                <div className="LName">
                    <p>BTC Forecasting</p>
                    <span>Hello World</span>
                </div>
              </div>
            </Link>
           
            {/* sidebar links */}
            <li className="nav-item my-1 mt-5">
              <NavLink className="nav-link sidebar-Link fw-500" to="/dashboard">
              <img className="" src={dashboardIco} alt="" />
                <span className="">Dashboard</span></NavLink>
            </li>
            <li className="nav-item my-1">
              <NavLink className="nav-link sidebar-Link fw-500" to="/loads">
                <img className="" src={cryptoIco} alt="" />
                <span className="">Crypto News</span></NavLink>
            </li>
            <li className="nav-item my-1">
              <NavLink className="nav-link sidebar-Link fw-500" to="/map">
                <img className="" src={publicIco} alt="" />
                <span className="">Public Sentiment</span></NavLink>
            </li>
         
           
          
            {/* Nav Item - Pages Collapse Menu */}
            {/* <li className="nav-item">
              <a className="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                <i className="fas fa-fw fa-cog" />
                <span>Components</span>
              </a>
              <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
                <div className="bg-white py-2 collapse-inner rounded">
                  <h6 className="collapse-header">Custom Components:</h6>
                  <a className="collapse-item" href="buttons.html">Buttons</a>
                  <a className="collapse-item" href="cards.html">Cards</a>
                </div>
              </div>
            </li> */}
           
           {/* <li className="logout-li">
               <a className="logout-div" href="#" >
                <img className="img-profile rounded-circle" src={profile} />
                <div className="profile-div align-self-center">
                  <span className="status ">Logout</span>
                </div>
              </a>
           </li> */}
          </ul>
          {/* End of Sidebar */}

        </>
    )
    
}
export default Sidebar