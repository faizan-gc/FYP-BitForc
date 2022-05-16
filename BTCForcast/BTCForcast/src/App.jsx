import React,{useEffect, useState} from 'react';
import { BrowserRouter, BrowserRouter as Router,Route,Switch } from "react-router-dom";

import './App.css'
import './component/global/global.css'
import './component/dashboard/dashboard.css'
import './component/dashboard/circle.css'
// import './component/loads/loads.css'
// import './component/drivers/drivers.css'

import $ from 'jquery';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/bootstrap/dist/js/bootstrap.min.js';
import '../node_modules/jquery/dist/jquery.min.js';
import '../node_modules/jquery.easing/jquery.easing';

import '../node_modules/popper.js/dist/popper'

// route
import  AppRouter from "./route/route";
import Sidebar from './component/global/sidebar/sidebar';
import Navbar from './component/global/navbar/navbar';


function App() {

  return (
    <>
          <BrowserRouter>
          <Router>
              {/* Page Wrapper */}
              <div id="wrapper">
                <Sidebar />
                  {/* Content Wrapper */}
                  <div id="content-wrapper" className="d-flex flex-column">
                    {/* Main Content */}
                    <div id="content">
                      <Navbar />

                    {/* Begin Page Content */}
                      <AppRouter />
                    {/* /.container-fluid */} 

                  </div>
                {/* End of Main Content */}
              </div>
              {/* End of Content Wrapper */}
            </div>
            {/* End of Page Wrapper */}

            {/* Scroll to Top Button*/}
            <a className="scroll-to-top rounded" href="#">
              <i className="fas fa-angle-up" />
            </a>
        </Router>
        </BrowserRouter>

     
    </>
  );
}

export {App};
