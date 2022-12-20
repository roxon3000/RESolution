import React from 'react';
import { Route, BrowserRouter, Routes } from 'react-router-dom';
import Home from './components/Home';
import Detail from './components/Detail';
import ObjectTree from './components/ObjectTree'
import ExampleTree from './components/ExampleTree'

class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <Routes>
                    <Route exact path="/" element={<Home />} />
                    <Route exact path="/detail" element={<Detail />} />
                    <Route exact path="/tree" element={<ObjectTree />} />
                    <Route exact path="/exampletree" element={<ExampleTree />} />
                </Routes>
            </BrowserRouter>
        );
    }
}

export default App;