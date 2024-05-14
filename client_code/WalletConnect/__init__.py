from ._anvil_designer import WalletConnectTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js import import_from
import anvil.server
import json
#anvil.js.report_all_exceptions(False, reraise=False)
createWeb3Modal = import_from("@web3modal/ethers5").createWeb3Modal
defaultConfig=import_from("@web3modal/ethers5").defaultConfig
ethers = import_from("ethers").ethers
pulsechain_url = "https://rpc.pulsechain.com"
ethereum_url = "https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"
class WalletConnect(WalletConnectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address=None
    self.provider=None
    self.mainnet = {
      "chainId": 1,
      "name": 'Ethereum',
      "currency": 'ETH',
      "explorerUrl": 'https://etherscan.io',
      "rpcUrl": ethereum_url
    }
    self.pulsechain = {
      "chainId": 369,
      "name": 'PulseChain',
      "currency": 'PLS',
      "explorerUrl": 'https://scan.pulsechain.com',
      "rpcUrl": pulsechain_url
    }
    self.degen = {
      "chainId": 666666666,
      "name": 'Degen Chain',
      "currency": 'DEGEN',
      "explorerUrl": 'https://explorer.degen.tips',
      "rpcUrl": "https://rpc.degen.tips"
    }
    self.base = {
      "chainId": 8453,
      "name": 'Base Mainnet',
      "currency": 'ETH',
      "explorerUrl": 'https://basescan.org',
      "rpcUrl": "https://mainnet.base.org"
    }
    self.metadata = {
      "name": properties['name'],
      "description": properties['description'],
      "url": anvil.server.get_app_origin(),
      "icons": [properties['icon']]
    }
    self.localhost = {
      "chainId": 31337,
      "name": 'Ethereum',
      "currency": 'ETH',
      "explorerUrl": 'https://etherscan.io',
      "rpcUrl": "http://127.0.0.1:8545/"
    }
    
    self.projectId=properties['project_id']
    print(properties['chain_ids'])
    self.chainIds = [int(i) for i in properties['chain_ids']]
    self.refreshModal()
  def refreshModal(self):
    self.default_chain = self.degen
    self.modal = createWeb3Modal({
    "ethersConfig": defaultConfig(self.metadata),
    "chains":list(app_tables.wallet_chains.search(chainId=q.any_of(*self.chainIds))),
    "projectId": self.projectId,
    "enableAnalytics": True,
    "defaultChain":self.default_chain })
  
    self.modal.subscribeProvider(self.handleChange)
    
  def establish_connection(self):
    self.address=None
    self.provider=None
    
    
    
    self.modal.open()
    
    
    
    
    
  def establish_connectionold(self):
    self.address=None
    self.provider=None
    if not is_ethereum:
      alert('Connect to browser supported by ethereum')
    else:
      try:
        self.provider = anvil.js.await_promise(ethers.providers.Web3Provider(ethereum))
        try:
          anvil.js.await_promise(ethereum.request({"method": 'eth_requestAccounts' }))
        except anvil.js.ExternalError as e:
          raise e
        self.signer= self.provider.getSigner()
        self.address=self.signer.getAddress()
      except Exception as e:
        raise e
    

  
    
  def handleChange(self, *args):
    
    _ = args[0]
    self.address = _.address
    self.chainId = _.chainId
    self.isConnected = _.isConnected
    if self.address is None:
      self.button_1.text = "connect wallet"
    else:
      self.button_1.text = "{}...{}".format(self.address[0:4], self.address[-4:])
    
    self.walletProvider = _.provider
   
    if self.walletProvider is not None:
      self.provider=anvil.js.await_promise(ethers.providers.Web3Provider(self.walletProvider))
      self.signer= self.provider.getSigner()
    else:
      self.signer = None
      self.provider = None
    
    self.raise_event("connect")
    #self.update_signer()
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.establish_connection()
    

