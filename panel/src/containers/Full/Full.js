import React, { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';
import { Container } from 'reactstrap';
import Header from '../../components/Header/';
import Sidebar from '../../components/Sidebar/';
import Aside from '../../components/Aside/';
import Footer from '../../components/Footer/';
import Dashboard from '../../views/Dashboard/';

import ShortcutsBar from '../../components/ShortcutsBar/ShortcutsBar';

import Usuarios from '../../views/Usuarios/Usuarios/';
import Permisos from '../../views/Usuarios/Permisos/';
import Grupos from '../../views/Usuarios/Grupos/';

import IdleTimer from 'react-idle-timer';

import auth from '../../auth/auth';

class Full extends Component {
  constructor(props) {
    super(props);
    this.state = {
      idle: false
    }
    this.idleTimer = null;
  }

  onIdle = e => {
    auth.logout();
    this.setState(() => ({
      idle: true
    }));
  }

  render() {
    if (this.state.idle) {
      return <Redirect to="/locked" />
    }

    return (
      <div className="app">
        <IdleTimer
          ref={ref => { this.idlerTimer = ref }}
          element={document}
          onIdle={this.onIdle}
          timeout={1000 * 60 * 30}
        > {/*30 Minutos*/}
          <Header />
          <div className="app-body">
            <Sidebar {...this.props} />
            <main className="main">
              <Container fluid>
                <Switch>
                  <Route path="/dashboard" name="Dashboard" component={Dashboard} />

                  <Route path="/usuarios/usuarios" name="Usuarios" component={Usuarios} />
                  <Route path="/usuarios/permisos" name="Permisos" component={Permisos} />
                  <Route path="/usuarios/grupos" name="Grupos" component={Grupos} />

                  <Redirect from="/" to="/dashboard" />
                </Switch>
              </Container>
            </main>
          </div>
          <ShortcutsBar />
        </IdleTimer>
      </div>
    );
  }
}

export default Full;
