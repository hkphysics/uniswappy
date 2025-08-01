# ─────────────────────────────────────────────────────────────────────────────
# Apache 2.0 License (DeFiPy)
# ─────────────────────────────────────────────────────────────────────────────
# Copyright 2023–2025 Ian Moore
# Email: defipy.devs@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

from abc import *

class Vault(ABC):
             
    @abstractmethod        
    def rebase_index_tkn(self, lp_token, token):
        pass
    @abstractmethod     
    def deposit_lp_tkn(self, _to, token, amt):
        pass    
    @abstractmethod     
    def remove_lp_tkn(self, _to, token, amt):
        pass
    @abstractmethod 
    def get_tkn_pair_amount(self, lp_tkn, tkn, liq):
        pass     
    @abstractmethod 
    def get_token_type(self, lp_tkn, tkn, liq):
        pass      