import React, {useEffect, useState } from 'react';
import { BrowserRouter,Redirect, BrowserRouter as Router,Route,Switch } from "react-router-dom";

import  {Dashboard}  from '../component/dashboard/dashboard';


function AppRouter(){

    return(
        <>
            <Route exact path='/'  >
                <Redirect to="/dashboard" />
            </Route>
            <Route exact path='/dashboard' component={Dashboard} />
            

        </>
    )
}

export default AppRouter