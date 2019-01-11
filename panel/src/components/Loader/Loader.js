import React, {Component} from 'react';
import "./loader.scss";

class Loader extends Component {
  render() {
    return (
      <div className="loader-backdrop">
        <div className="loader">
        </div>
      </div>
    )
  }
}

export default Loader;
