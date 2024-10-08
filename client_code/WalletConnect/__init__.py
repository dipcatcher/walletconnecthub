from ._anvil_designer import WalletConnectTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from anvil.js import import_from
import anvil.server
import json
#from anvil.js.window import ethers

#anvil.js.report_all_exceptions(False, reraise=False)
createWeb3Modal = import_from("@web3modal/ethers5").createWeb3Modal
defaultConfig=import_from("@web3modal/ethers5").defaultConfig
ethers = import_from("ethers").ethers

class WalletConnect(WalletConnectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.address=None
    self.provider=None
    self.signer=None
    
    self.metadata = {
      "name": properties['name'],
      "description": properties['description'],
      "url": anvil.server.get_app_origin(),
      "icons": [properties['icon']]
    }
  
    
    self.projectId=properties['project_id']
    self.chainIds = [int(i) for i in properties['chain_ids']]
    self.chains =  [dict(r) for r in app_tables.wallet_chains.search(chainId=q.any_of(*self.chainIds))]
    print(self.chains)
    if self.chains ==[]:
      self.chains = [dict(r) for r in app_tables.wallet_chains.search(chainId=1)]
    print(self.projectId)
    if self.projectId in [None, ""]:
      self.projectId = "7f21244f1b374588fbdb25f07864d5cd"
    self.refreshModal()
  def refreshModal(self):
    self.default_chain = self.chains[0]
    self.modal = createWeb3Modal({
    "ethersConfig": defaultConfig(self.metadata),
    "chains":self.chains,
    "projectId": self.projectId,
    "enableAnalytics": True,
    "enableOnramp":True,
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
    c = app_tables.wallet_chains.get(chainId=self.chainId)
    print(self.chainId)
    if c is not None:
      self.link_1.icon = c['logo'].get_url()
    else:
      self.link_1.icon = None
    self.raise_event("connect")
    #self.update_signer()
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.establish_connection()

  def drop_down_chains_change(self, **event_args):
    """This method is called when an item is selected"""
    a = event_args['sender'].selected_value

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.modal.open({"view":"Networks"})
    

