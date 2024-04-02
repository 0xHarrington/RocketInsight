import React, { useState } from 'react';
import LineGraph from './graph.js';
import NetworkGraph from './network.js';
import axios from 'axios';
import { Container } from 'react-bootstrap';
import './style.css'

function Pages() {
  const [showpage, setShowpage] = useState(1);

  const handlepage = (e) => {
    setShowpage(e);
  }
  return (
    <div id="page-formatting">
      <nav>
        <div className="marginals">
          <div className="VTEE">
            RocketInsight
          </div>
          <ul>
            <li><button className={showpage === 1 ? "nav-link active" : "nav-link"} onClick={() => handlepage(1)}>Markets</button></li>
            <li><button className={showpage === 2 ? "nav-link active" : "nav-link"} onClick={() => handlepage(2)}>Wallets</button></li>
          </ul>
          <div className="login">
            <ul>
              <li><a href="#">FAQ</a></li>
              <li><a href="#">Contact Us</a></li>
            </ul>
          </div>
        </div>
      </nav>

      <React.Fragment>
        <Container>

          <div className="page">

            <div className={showpage === 1 ? "landing fade show active" : "landing fade"}>
              <main id="l-products">
                <h1>Welcome to RocketInsight</h1>
                <br />
                <div className="subheading">
                  <h3 align="center">Statistics, analytics and more, to help you make informed decisions with your rEth.</h3>
                </div>
                <br />
                <LineGraph />
                <br />
                <h2 align="center">Protocols with rEth Assets</h2>
                <br />
                <br />
                <table>
                  <tr>
                    <td>
                      <div className="thead">
                        Protocol
                      </div>
                    </td>
                    <td>
                      <div className="thead">
                        URL
                      </div>
                    </td>
                    <td>
                      <div className="thead">
                        Total Supplied
                      </div>
                    </td>
                    <td>
                      <div className="thead">
                        Total Borrowed
                      </div>
                    </td>
                    <td>
                      <div className="thead">
                        Supply APY
                      </div>
                    </td>
                    <td>
                      <div className="thead">
                        Borrow APY
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <a className={showpage === 3 ? "nav-link active" : "nav-link"} onClick={() => handlepage(3)}><img src="logo1.jpeg" /></a>
                    </td>
                    <td><a href="https://app.aave.com/reserve-overview/?underlyingAsset=0xae78736cd615f374d3085123a210448e74fc6393&marketName=proto_mainnet_v3">AAVE</a></td>
                    <td>
                      47.68K
                    </td>
                    <td>
                      74.86K
                    </td>
                    <td>
                      0.01%
                    </td>
                    <td>
                      0.01%
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <img src="logo2.png" />
                    </td>
                    <td>
                      <a href="https://app.compound.finance/markets/weth-mainnet">Compound</a>
                    </td>
                    <td>
                      47.68K
                    </td>
                    <td>
                      74.86K
                    </td>
                    <td>
                      0.01%
                    </td>
                    <td>
                      0.01%
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <img src="logo3.png" />
                    </td>
                    <td>
                      <a href="https://app.uniswap.org/explore/tokens/ethereum/0xae78736cd615f374d3085123a210448e74fc6393">Uniswap</a>
                    </td>
                    <td>
                      47.68K
                    </td>
                    <td>
                      74.86K
                    </td>
                    <td>
                      0.01%
                    </td>
                    <td>
                      0.01%
                    </td>
                  </tr>
                </table>
              </main>
            </div>

            <div className={showpage === 3 ? "market fade show active" : "market fade"}>
              <br />
              <div id="firstupper">
                <img src="aave.jpeg" />
                <br />
                <br />
                <a href="#">Back</a>
              </div>
              <div id="restupper">
                <table id="m-info">
                  <tr>
                    <td>
                      Total Borrowed:
                      <br />
                      498.08/19200
                    </td>
                    <td>
                      Total Supplied:
                      <br />
                      47.68K/90K
                    </td>
                    <td>
                      Utilization Rate:
                      <br />
                      1.04%
                    </td>
                  </tr>
                </table>
              </div>

              <aside id="options">
                <h4>Metrics</h4>
                <br />
                <form className="select-category">
                  <input type="checkbox" id="cat1" name="cat1" value="C1" />
                  <label for="cat1"> Net Price Deviation</label><br />
                  <input type="checkbox" id="cat2" name="cat2" value="C2" />
                  <label for="cat2"> Median APY</label><br />
                  <input type="checkbox" id="cat3" name="cat3" value="C3" />
                  <label for="cat3"> Historical Leverage</label><br />
                  <input type="checkbox" id="cat4" name="cat4" value="C4" />
                  <label for="cat4"> Price</label><b />
                </form>
              </aside>
              <aside id="graph">
                <img src="download.png" />
              </aside>
              <main id="products">
                <h1>Notable Activity</h1>
                <br />
                <table>
                  <tr>
                    <td>
                      <div class="thead">
                        <div class="firstc">
                          #
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="thead">
                        Wallet Address
                      </div>
                    </td>
                    <td>
                      <div class="thead">
                        Amount Leveraged
                      </div>
                    </td>
                    <td>
                      <div class="thead">
                        Risk Factor
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        1
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="positive">
                        3
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        2
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="negative">
                        9
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        3
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="positive">
                        3
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        4
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="positive">
                        0
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        5
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="positive">
                        2
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <div class="firstc">
                        6
                      </div>
                    </td>
                    <td>
                      0x52cF14DEc4b7B18454e6e5D543551d7A55F15805
                    </td>
                    <td>
                      -
                    </td>
                    <td>
                      <div class="negative">
                        10
                      </div>
                    </td>
                  </tr>
                </table>
              </main>
            </div>

            <div className={showpage === 2 ? "wallet fade show active" : "wallet fade"}>
              <main id="c-products">
                <br />
                <br />
                <h1>Wallet address clustering</h1>
                <br />
                <br />
                <aside id="c-options">
                  <br />
                  <form class="select-category">
                    <input type="checkbox" id="cat1" name="cat1" value="C1" />
                    <label for="cat1"> Show all transactions</label><br />
                    <input type="checkbox" id="cat2" name="cat2" value="C2" />
                    <label for="cat2"> Visualization Option 1</label><br />
                    <input type="checkbox" id="cat3" name="cat3" value="C3" />
                    <label for="cat3"> Visualization Option 2</label><br />
                  </form>
                </aside>
                <div id="search">
                  <h2>Enter Wallet Address:</h2>
                  <form action="#" method="GET">
                    <input type="text" id="lookup" name="search" placeholder="0x52cF14DEc4b7B18454e6e5D543551d7A55F15805" />
                    < input type="submit" value="Go" />
                  </form>
                </div>
                <div id="cluster">
                  <h2>Cluster:</h2>
                  <NetworkGraph />
                  <br />
                  
                </div>
              </main>
            </div>
          </div>
        </Container>

      </React.Fragment>
    </div>

  );
}

export default Pages