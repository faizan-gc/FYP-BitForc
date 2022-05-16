import React from "react";
 
import searchIco from "../../../images/searchIco.svg";
import profile from "../../../images/profile.jpg";
import dropdownIcon from "../../../images/dropdown-icon.svg";


function Navbar() {
    return(
        <>
             {/* Topbar */}
             <nav className="navbar navbar-expand navbar-light bg-theme topbar mb-4 static-top">
                {/* Sidebar Toggle (Topbar) */}
                <button id="sidebarToggleTop" className="btn btn-link d-md-none rounded-circle mr-3">
                  <i className="fa fa-bars" />
                </button>
                {/* Topbar Search */}
                <form className="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                  <div className="input-group">
                    <div className="input-group-append">
                      <button className="btn search-btn pr-0" type="button">
                        <img src={searchIco} className="w-15 mb-1" alt="serach icon" />
                      </button>
                    </div>
                    <input type="text" className="form-control theme-bg-color border-0 small" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2" />
                  </div>
                </form>
                {/* Topbar Navbar */}
              
              </nav>
              {/* End of Topbar */}
        </>
    )
    
}
export default Navbar