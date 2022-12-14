import React from 'react';
import { Route, BrowserRouter, Switch } from 'react-router-dom';
import Home from './components/Home';
import Detail from './components/Detail';
import ObjectTree from './components/ObjectTree'

class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/detail" component={Detail} />
                    <Route exact path="/tree" component={ObjectTree} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;