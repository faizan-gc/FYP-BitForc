import React,{useEffect,useState} from 'react';
import { Link } from "react-router-dom";

import {LineChart,Line,XAxis,YAxis,CartesianGrid,Tooltip,Legend,ReferenceLine,ResponsiveContainer} from 'recharts';

import revenue from "../../images/revenue.svg";
import truck from "../../images/truck.svg";
import averageRate from "../../images/average-rate.svg";
import loadMove from "../../images/load-move.svg";
import kebab from "../../images/kebab.svg";
import setting from "../../images/setting.svg";
import percIcon from "../../images/percIcon.svg";
import greaterIco from "../../images/greaterIco.svg";
import arrowDown from "../../images/arrowDown.svg";
import filterIcon from "../../images/filterIcon.svg";
import profile from "../../images/profile.jpg";


// import axios from "axios";



// js

// import Navbar from './navbar';
// import Sidebar from './sidebar';

function Dashboard(props) {
  const redColor={
    color:'red'
  }
  const greenColor={
    color:'#28CB89'
  }

  return(
    <>
                {/* Begin Page Content */}
                <div className="container-fluid">
                  
                    {/* Content Row */}
                    <div className="row dashbordTitle">
                      <div className="col">
                        <h2>Dashboard</h2>
                        <div className='goodDiv'>
                          <p>Good to see you</p>
                          <div className='customize'>
                            <span>Customize</span>
                            <img src={setting} alt="" />
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Content Row */}
                    <div className="row analyticsMainRow mx-0">
                    {/* Area Chart */}
                    <div className="col-xl-9 col-lg-8">
                      <div className="card analyticsCard br-10 h-100 border-transparent overflow-hidden">
                        {/* Card Header - Dropdown */}
                        <div className="card-header flexWrap border-transparent py-3 d-flex flex-row align-items-center justify-content-between">
                          <h6 className="m-0 chart-heading">Price Forecasting & Actual current price</h6>
                          <div className="dropdown no-arrow">
                              {/* <a href="#" className="chart-time chart-time-active pr-4">All time</a>
                              <a href="#" className="chart-time pr-4">This year</a>
                              <a href="#" className="chart-time pr-4">This week</a> */}

                              <a className="dropdown-toggle monthly mr-2" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <img src={filterIcon} className="mr-2" alt="dropdown icon" />
                                Filter
                                <img src={arrowDown} className="ml-2" alt="dropdown icon" />
                              </a>
                              <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                                <a className="dropdown-item" href="#">Action</a>
                                <a className="dropdown-item" href="#">Another action</a>
                                <div className="dropdown-divider" />
                                <a className="dropdown-item" href="#">Something else here</a>
                              </div>
                              <a className="dropdown-toggle monthly" href="#" role="button" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                Monthly
                                <img src={arrowDown} className="ml-2" alt="dropdown icon" />
                              </a>
                              <div className="dropdown-menu dropdown-menu-right shadow animated--fade-in" aria-labelledby="dropdownMenuLink">
                                <a className="dropdown-item" href="#">Action</a>
                                <a className="dropdown-item" href="#">Another action</a>
                                <div className="dropdown-divider" />
                                <a className="dropdown-item" href="#">Something else here</a>
                              </div>
                          </div>
                        </div>
                        {/* Card Body */}
                        <div className="card-body">
                          <div className="chart-area">
                              <RevenueChart />                    

                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* diver status */}
                    <div className="col-xl-3 col-lg-4">
                      <div className="dashPriceMain">
                        <div className="priceMain">
                          <h1>$61900</h1>
                          <p>Current Price 
                            {/* <span className='perc'>56% <img src={percIcon} alt="" /></span> */}
                            </p>
                          <button className='btn chartBtn'>See Detailed Chart 
                            <span> <img src={greaterIco} alt="" /></span>
                          </button>
                        </div>
                        <div className="priceMain mt-5">
                          <h1>$61900</h1>
                          <p>Current Price <span className='acc'>78%</span></p>
                          <button className='btn chartBtn'>Previous Results
                            <span> <img src={greaterIco} alt="" /></span>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="publicCentMain">
                    <h5>Public Sentiment</h5>
                    <div class="clearfix">

                      <div class="c100 p20">
                        <span>25%</span>
                        <div class="slice">
                            <div class="bar"></div>
                            <div class="fill"></div>
                        </div>
                    </div>
                    </div>
                  </div>
            
                </div>
                {/* /.container-fluid */}
       
    </>
  )
}


function DriverStatusRow(props) {
  return(
      <div className="d-flex py-2 driver-dash-div flex-row align-items-center justify-content-between">
        <div className="d-flex">
          <img className="driver-img rounded-circle" src={props.profileImg} />
            <div className="profile-div ml-2">
              <span className="mr-2 fs-14 small profile-name">{props.driverName}</span>
              <span className="status fs-10 font-weight-bold dark-font">{props.company}</span>
            </div>
        </div>
        <div>
          {/* this condition check status and set specified color */}
          {props.status == "Loaded" && props.status != "Waiting" ?<span className="driver-status-title status-loaded">{props.status}</span>
          : props.status == "Waiting" && props.status != "Loaded"?<span className="driver-status-title status-waiting">{props.status}</span>
          :<span className="driver-status-title status-offline">{props.status}</span>
          }
        </div>
     </div>
  )
  
}

function RevenueChart() {
  const data = [
    {
      name: 'Jan',
      AG: 40,
      PG: 24,
      amt: 2400,
    },
    {
      name: 'Feb',
      AG: 10,
      PG: 13,
      amt: 2210,
    },
    {
      name: 'Mar',
      AG: 90,
      PG: 98,
      amt: 2290,
    },
    {
      name: 'Apr',
      AG: 120,
      PG: 110,
      amt: 2000,
    },
   
    {
      name: 'May',
      AG: 100,
      PG: 90,
      amt: 2500,
    },
    {
      name: 'Jun',
      AG: 34,
      PG: 43,
      amt: 2100,
    },
    {
      name: 'Jul',
      AG: 34,
      PG: 43,
      amt: 2100,
    },
    {
      name: 'Aug',
      AG: 34,
      PG: 43,
      amt: 2100,
    },
    {
      name: 'Sep',
      AG: 44,
      PG: 53,
      amt: 2100,
    },
    {
      name: 'Oct',
      AG: 84,
      PG: 13,
      amt: 2100,
    },
    {
      name: 'Nov',
      AG: 44,
      PG: 23,
      amt: 2100,
    },
    {
      name: 'Dec',
      AG: 34,
      PG: 53,
      amt: 2100,
    },
  ];
  return(
    <ResponsiveContainer width="100%" height="100%">
    <LineChart width={500} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" padding={{ left: 30, right: 30 }} />
      <YAxis  />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="AG" stroke="#8884d8" activeDot={{ r: 8 }} />
      <Line type="monotone" dataKey="PG" stroke="#82ca9d" />
    </LineChart>
  </ResponsiveContainer>
   

  
  )
  
}


export {Dashboard};
