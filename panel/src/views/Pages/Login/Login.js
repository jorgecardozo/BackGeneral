import React, { Component } from 'react';
import { Container, Row, Col, Form, FormGroup, Label, Input, Button, Alert } from 'reactstrap';
import auth from '../../../auth/';

import './Login.css';

class Login extends Component {
	constructor(props) {
		super(props);
		this.state = {
			dniCuit: '',
			recordarDniCuit: false,
			username: '',
			password: '',
			showPassword: false,
			showError: false,
			isLoading: false
		}
	}

	componentDidMount() {
		const dniCuit = localStorage.getItem('dni_cuit');
		if (dniCuit) {
			this.setState(_ => ({
				dniCuit,
				recordarDniCuit: true
			}));
		}
	}

	login = (e) => {
		e.preventDefault();

		this.setState(_ => ({ isLoading: true }));

		const { username, password, dniCuit } = this.state;
		auth.login(username, password, dniCuit, response => {
			if (response.success) {
				if (this.state.recordarDniCuit) {
					localStorage.setItem('dni_cuit', this.state.dniCuit);
				} else {
					localStorage.removeItem('dni_cuit');
				}
				this.props.history.push('/');
			} else {
				this.setState(_ => ({ showError: true, isLoading: false }));
			}
		});
	}

	onDniCuitChange = e => {
		e.persist();
		const { value } = e.target
		if (value.length <= 11 && /^[0-9]*$/.test(value)) {
			this.setState(prevState => ({
				showError: false,
				dniCuit: value
			}));
		}
	}

	onRecordarDniCuitChange = e => {
		e.persist();
		this.setState(prevState => ({
			recordarDniCuit: e.target.checked
		}));
	}

	onUsernameChange = e => {
		e.persist();
		this.setState(prevState => ({
			showError: false,
			username: e.target.value
		}));
	}

	onPasswordChange = e => {
		e.persist();
		this.setState(prevState => ({
			showError: false,
			password: e.target.value
		}));
	}

	onShowPassword = e => {
		e.persist();
		this.setState(() => ({
			showPassword: e.type === 'mousedown'
		}));
	}

	render() {
		return (
			<div className="login-page w-100 h-100 position-absolute">
				<Container className="d-flex flex-column justify-content-center h-100" >
					<Row className="justify-content-center px-3 px-md-0">
						<Col xs="12" lg="6" xl="6">{/* Imagen */}</Col>
						<Col xs="12" lg="6" xl="5" className="login-form px-4 py-5 px-md-5">
							<img src="img/logoBorniego.png" alt="Logo de la empresa" />
							<div className="logo-borniego"></div>
							<hr />
							<Form
								onSubmit={this.login}
							>
								<FormGroup>
									<Label for="dniCuit">DNI/ CUIT</Label>
									<Row>
										<Col xs="12" md="8">
											<Input
												id="dniCuit"
												type="text"
												value={this.state.dniCuit}
												onChange={this.onDniCuitChange}
											/>
										</Col>
										<Col xs="12" md="4">
											<Label check>
												<Input
													type="checkbox"
													checked={this.state.recordarDniCuit}
													onChange={this.onRecordarDniCuitChange}
												/>
												Recordar
                                            </Label>
										</Col>
									</Row>
								</FormGroup>

								<FormGroup>
									<Label for="username">Nombre de usuario ó email</Label>
									<Input
										id="username"
										type="text"
										value={this.state.username}
										onChange={this.onUsernameChange}
									/>
								</FormGroup>
								<FormGroup>
									<Label for="password">Contraseña</Label>
									<div className="password">
										<Input
											id="password"
											type={this.state.showPassword ? 'text' : 'password'}
											value={this.state.password}
											onChange={this.onPasswordChange}
										/>
										<Button
											onClick={e => e.preventDefault()}
											onMouseDown={this.onShowPassword}
											onMouseUp={this.onShowPassword}
											className="password__show-pw"
										>
											<i className={'fa ' + (!this.state.showPassword ? 'fa-eye' : 'fa-eye-slash')}></i>
										</Button>
									</div>

								</FormGroup>

								{this.state.showError &&
									<Alert color="danger">
										El usuario y/o contraseña son incorrectos.
                                    </Alert>
								}
								<div className="text-right">
									{this.state.isLoading &&
										<img className="mr-2" src="img/loader.gif" alt="Espere..." />
									}
									<Button className="btn-submit d-inline ml-auto "
										disabled={this.state.username && this.state.password && this.state.dniCuit != '' ? false : true}
									>
										{this.state.isLoading ? 'Iniciando sesión...' : 'Iniciar sesión'}
									</Button>
								</div>
							</Form>
						</Col>
					</Row>
				</Container>

				<footer className="login-footer">
					<div className="float-right">© 2018</div>
					<div className="logoParadigma"></div>
				</footer>
			</div>
		);
	}
}

export default Login;