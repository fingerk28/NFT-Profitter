from flask import Flask
from flask import render_template, request
from etherscan import Etherscan
from web3 import Web3
from collections import defaultdict
from collections import Counter
from collections import OrderedDict
import operator
import requests
import json
import time
from tqdm import tqdm


ether_api_key = 'H6P4TI21N8TMHQMN7BY9PKNWXWIBB6Y2VA'
eth = Etherscan(ether_api_key)
abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"ApprovalToCurrentOwner","type":"error"},{"inputs":[],"name":"ApproveToCaller","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"InvalidQueryRange","type":"error"},{"inputs":[],"name":"InvalidToken","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"NotAuthorized","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"approved","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"operator","type":"address"},{"indexed":False,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":True,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"explicitOwnershipOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"}],"internalType":"struct ERC721A.TokenOwnership","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],"name":"explicitOwnershipsOf","outputs":[{"components":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"uint64","name":"startTimestamp","type":"uint64"},{"internalType":"bool","name":"burned","type":"bool"}],"internalType":"struct ERC721A.TokenOwnership[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"isTokenValid","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"quantity","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextTokenId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"numBurnedOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"numMintedOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"provenanceMerkleRoot","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint256","name":"_salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"addr","type":"address"},{"internalType":"bool","name":"isAuthorized","type":"bool"}],"name":"setAuthorized","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"baseTokenURI","type":"string"}],"name":"setBaseTokenURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint96","name":"feeNumerator","type":"uint96"}],"name":"setDefaultRoyalty","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"root","type":"bytes32"}],"name":"setProvenanceMerkleRoot","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"setTokenInvalid","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint96","name":"feeNumerator","type":"uint96"}],"name":"setTokenRoyalty","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"setTokenValid","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"tokensOfOwner","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"start","type":"uint256"},{"internalType":"uint256","name":"stop","type":"uint256"}],"name":"tokensOfOwnerIn","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"metadataId","type":"uint256"},{"internalType":"string","name":"cid","type":"string"},{"internalType":"bytes32[]","name":"merkleProofs","type":"bytes32[]"}],"name":"verifyProvenance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route("/select_address", methods=['GET', 'POST'])
def select_records():
    if request.method == 'POST':
        erc721_dict, trade_info, leaderboard = get_transactions(request.form['address'].lower())
        total_gas = get_gas(request.form['address'].lower())
        return render_template("result.html", nft_dict=erc721_dict, trade_info=trade_info, leaderboard=leaderboard, total_gas=total_gas)
    else:
        return render_template("home.html")

@app.route("/whale_tracking", methods=['GET', 'POST'])
def whale_tracking():
    if request.method == 'POST':
        addr_list = [request.form['address1'], request.form['address2'], request.form['address3'], request.form['address4'], request.form['address5']]
        addr_list = [addr for addr in addr_list if addr != '']
        whale_dict = frequent_trader_analysis(addr_list, eval(request.form['trader_num']))
        return render_template("whale.html", whale_dict=whale_dict)
    else:
        return render_template("home.html")

def get_gas(address):
    transactions = eth.get_normal_txs_by_address(address, 0, 999999999, 'asc')
    total_gas = 0
    for t in transactions:
        gas_fee = float(t['gasPrice']) * float(t['gasUsed']) / 1e18
        total_gas += gas_fee
    return round(total_gas, 2)

def get_tx_info(WALLET_ADDRESS):
    print("Get etherscan data from wallet '{}'...".format(WALLET_ADDRESS))
    eth_last_price = eth.get_eth_last_price()
    latest_block_number = eth.get_block_number_by_timestamp(timestamp=eth_last_price['ethusd_timestamp'], closest="before")
    all_transactions = eth.get_normal_txs_by_address(WALLET_ADDRESS, startblock=0, endblock=latest_block_number, sort='asc')
    all_transactions_dict = {all_transactions[i]['hash']: all_transactions[i] for i in range(len(all_transactions))}
    erc721_transactions = eth.get_erc721_token_transfer_events_by_address(WALLET_ADDRESS, startblock=0, endblock=latest_block_number, sort='asc')

    try:
        internal_transactions = eth.get_internal_txs_by_address(WALLET_ADDRESS, startblock=0, endblock=latest_block_number, sort='asc')
        internal_transactions_dict = {internal_transactions[i]['hash']: internal_transactions[i] for i in range(len(internal_transactions))}
    except:
        pass

    try:
        erc20_transactions = eth.get_erc20_token_transfer_events_by_address(WALLET_ADDRESS, startblock=0, endblock=latest_block_number, sort='asc')
        erc20_transactions_dict = {}
        for i in range(len(erc20_transactions)):
            if erc20_transactions_dict.__contains__(erc20_transactions[i]['hash']):
                if float(erc20_transactions[i]['value']) > float(erc20_transactions_dict[erc20_transactions[i]['hash']]['value']):
                    erc20_transactions_dict[erc20_transactions[i]['hash']]['value'] = float(erc20_transactions[i]['value']) - float(erc20_transactions_dict[erc20_transactions[i]['hash']]['value'])
                else:
                    erc20_transactions_dict[erc20_transactions[i]['hash']]['value'] = float(erc20_transactions_dict[erc20_transactions[i]['hash']]['value']) - float(erc20_transactions[i]['value'])
            else:
                erc20_transactions_dict[erc20_transactions[i]['hash']] = erc20_transactions[i]
    except:
        erc20_transactions_dict = {}
        pass
    print('------------------------------')
    return erc721_transactions,all_transactions_dict, internal_transactions_dict,erc20_transactions_dict

def get_floor_price(contract_address, item, WALLET_ADDRESS):
    url = 'https://api.opensea.io/api/v1/collections?asset_owner={}&offset=0&limit=300'.format(WALLET_ADDRESS)
    res = requests.get(url)
    text = json.loads(res.text)

    slug = None
    for i in range(len(text)):
        try:
            addr = text[i]['primary_asset_contracts'][0]['address']
            #print(text[i]['slug'])
            if addr == contract_address:
                #print(text[i]['slug'])
                slug = text[i]['slug']
                break
        except:
            pass
    if slug == None:
        slug = item.replace(' ', '')
        slug = slug.lower()
    url = 'https://api.opensea.io/api/v1/collection/{}/stats'.format(slug)
    res = requests.get(url)
    if res:
        return json.loads(res.text)['stats']['floor_price']
    else:
        return -1

def cal_gas(meta):
    gas_price = eval(meta['gasPrice'])
    gas_used = eval(meta['gasUsed'])
    return gas_price * gas_used / 1e18

def get_value(value):
    return float(value) / 1e18

def download_image(imageUrl, filename):
    res = requests.get(imageUrl)
    img_data = res.content
    if res.status_code == 200:
        with open('./images/'+filename,'wb') as f:
            f.write(img_data)
            print('Image sucessfully Downloaded: ',filename)
    else:
        print('Image Couldn\'t be retrieved')

def get_nft_image(contract_address, tokenId, itemName):
    url =  'https://eth-mainnet.alchemyapi.io/v2/demo/getNFTMetadata?contractAddress=' + contract_address + '&tokenId=' + tokenId+'&tokenType=erc721'
    flag = False
    for i in range(10):
        res = requests.get(url)
        if (res.status_code==200):
            flag = True
            break
    res = json.loads(res.text)
    if res['media'][0]['gateway']=='':
        imageUrl = get_nft_image_alternative(contract_address, tokenId, itemName)
    else:
        imageUrl = res['media'][0]['gateway']
        print(imageUrl)
    return imageUrl

def get_nft_image_alternative(contract_address, tokenId, itemName):
    global web3
    address = Web3.toChecksumAddress(contract_address)
    contract = web3.eth.contract(address=address, abi=abi)
    metaURL = contract.functions.tokenURI(int(tokenId)).call()
    headers = {"Accept": 'application/json'}
    imageUrl = None
    if "http" == metaURL[0:4]:
        flag = False
        for i in range(10):
            time.sleep(0.5)
            res = requests.get(metaURL)
            if (res.status_code==200):
                flag = True
                break
        if flag:
            res = json.loads(res.text)
            for k, v in res.items():
                if "image" in k:
                    imageUrl = v
                    break
    else:
        metaURL = metaURL.replace('ipfs://', '')
        if 'ipfs' == metaURL[0:4]:
            metaURL = metaURL.replace('ipfs/', '')
        metaURL = "https://ipfs.io/ipfs/" + metaURL
        flag = False
        for i in range(10):
            time.sleep(0.5)
            res = requests.get(metaURL)
            if (res.status_code==200):
                flag = True
                break
        if flag:
            res = json.loads(res.text)
            for k, v in res.items():
                if "image" in k:
                    imageUrl = v
                    break
    if imageUrl == None:
        print('No image url is found')
        return -1

    if "http" == imageUrl[0:4]:
        print(imageUrl)
        filename = itemName + '_#' + tokenId + '.jpg'
        #download_image(imageUrl, filename)
        
    else:
        imageUrl = imageUrl.replace('ipfs://', '')
        if 'ipfs' == imageUrl[0:4]:
            imageUrl = imageUrl.replace('ipfs/', '')
        imageUrl = "https://ipfs.io/ipfs/" + imageUrl
        print(imageUrl)
        filename = itemName + '_#' + tokenId + '.jpg'
        #download_image(imageUrl, filename)
    return imageUrl

def get_buy_sell_history(erc721_dict, erc721_transactions, all_transactions_dict, internal_transactions_dict,erc20_transactions_dict,WALLET_ADDRESS):
    print('Get NFT buy & sell history...')
    for trx in erc721_transactions:
        token_name = trx['tokenName']
        trx_hash = trx['hash']
        if trx['to'] == WALLET_ADDRESS and all_transactions_dict.__contains__(trx_hash):
            if erc721_dict[token_name].__contains__(trx['tokenID']):
                continue
            erc721_dict[token_name][trx['tokenID']] = {'hash': trx_hash,
                                                        'buy_price': round(get_value(all_transactions_dict[trx_hash]['value']), 3),
                                                        'gas_fee': cal_gas(all_transactions_dict[trx_hash]),
                                                        'contract_address': trx['contractAddress']}
            print('Item: {}, Token ID: {}, buy_price: {:.3f}'.format(token_name, trx['tokenID'], get_value(all_transactions_dict[trx_hash]['value'])))
        
        elif trx['to'] == WALLET_ADDRESS and erc20_transactions_dict.__contains__(trx_hash):
            if erc721_dict[token_name].__contains__(trx['tokenID']):
                continue
            erc721_dict[token_name][trx['tokenID']] = {'hash': trx_hash,
                                                        'buy_price': round(get_value(erc20_transactions_dict[trx_hash]['value']), 3),
                                                        'gas_fee': cal_gas(erc20_transactions_dict[trx_hash]),
                                                        'contract_address': trx['contractAddress']}
            print('Item: {}, Token ID: {}, buy_price: {:.3f}'.format(token_name, trx['tokenID'], get_value(erc20_transactions_dict[trx_hash]['value'])))

        elif internal_transactions_dict.__contains__(trx_hash) and erc721_dict[token_name].__contains__(trx['tokenID']):
            erc721_dict[token_name][trx['tokenID']]['sell_price'] = get_value(internal_transactions_dict[trx_hash]['value'])
            print('Item: {}, Token ID: {}, sell_price: {:.3f}'.format(token_name, trx['tokenID'], get_value(internal_transactions_dict[trx_hash]['value'])))
        
        elif erc20_transactions_dict.__contains__(trx_hash) and erc721_dict[token_name].__contains__(trx['tokenID']):
            erc721_dict[token_name][trx['tokenID']]['sell_price'] = get_value(erc20_transactions_dict[trx_hash]['value'])
            print('Item: {}, Token ID: {}, sell_price: {:.3f}'.format(token_name, trx['tokenID'], get_value(erc20_transactions_dict[trx_hash]['value'])))
    for item, item_dict in erc721_dict.items():
        tmp_dict = defaultdict(int)
        for token_id, meta in item_dict.items():
            tmp_dict[meta['hash']] += 1
        for token_id, meta in item_dict.items():
            meta['buy_price'] /= tmp_dict[meta['hash']]
            meta['gas_fee'] /= tmp_dict[meta['hash']]
    print('------------------------------')

def get_opensea_floor_price(erc721_dict, WALLET_ADDRESS):
    print('Get Opensea floor price...')
    del_list = []
    for item, item_dict in erc721_dict.items():
        for k, v in item_dict.items():
            if not v.__contains__('sell_price'):
                #print(v['contract_address'])
                item_dict[k]['floor_price'] = get_floor_price(v['contract_address'], item, WALLET_ADDRESS)
                if item_dict[k]['floor_price'] in [-1, None]:
                    del_list.append((item, k))
        try:
            if item_dict[k].__contains__('floor_price'):
                print(item, item_dict[k]['floor_price'])
        except:
            pass
    print('------------------------------')

    for item, token_id in del_list:
        print('Deleting {}, token id: {}...'.format(item, token_id))
        del erc721_dict[item][token_id]
    print('------------------------------')

def get_history_transacted_images(erc721_dict):
    print('Get history transacted images...')
    for item, item_dict in erc721_dict.items():
        print(item)
        for k, v in item_dict.items():
            contract_address = v['contract_address']
            break
        for token in item_dict.keys():
            print(token)
            # try:
            image_url = get_nft_image(contract_address, token, item)
            item_dict[token]['image_url'] = image_url
            # except:
            #     print('Error')
            #     item_dict[token]['image_url'] = -1
    print('------------------------------')

def calculat_cost_and_income(erc721_dict, WALLET_ADDRESS):
    print('Calculate cost and income...')
    
    realized_income = 0.
    realized_cost = 0.
    unrealized_income = 0.
    unrealized_cost = 0.
    net_profits = []
    for item, item_dict in erc721_dict.items():
        net_profit = 0.
        for k, v in item_dict.items():
            if v.__contains__('sell_price'):
                realized_income += v['sell_price']
                realized_cost += v['buy_price'] + v['gas_fee']
                net_profit += (v['sell_price'] - v['buy_price'] - v['gas_fee'])
            else:
                unrealized_income += v['floor_price']
                unrealized_cost += v['buy_price'] + v['gas_fee']
                net_profit += (v['floor_price'] - v['buy_price'] - v['gas_fee'])
        net_profits.append([item, net_profit])
    net_profits = sorted(net_profits, key=lambda x: x[1], reverse=True)
    print('------------------------------')

    trade_info = {}
    trade_info['address'] = WALLET_ADDRESS
    trade_info['Realized income'] = f'{realized_income:.3f}'
    trade_info['Realized cost'] = f'{realized_cost:.3f}'
    trade_info['Realized profit'] = f'{(realized_income - realized_cost):.3f}'

    trade_info['Unrealized income'] = f'{unrealized_income:.3f}'
    trade_info['Unrealized cost'] = f'{unrealized_cost:.3f}'
    trade_info['Unrealized profit'] = f'{(unrealized_income - unrealized_cost):.3f}'

    trade_info['Total income'] = f'{(realized_income + unrealized_income):.3f}'
    trade_info['Total cost'] = f'{(realized_cost + unrealized_cost):.3f}'
    trade_info['Total profit'] = f'{(realized_income + unrealized_income - realized_cost - unrealized_cost):.3f}'

    leaderboard = []
    num_win_items = 0.
    num_loss_items = 0.
    for i in range(len(net_profits)):
        if i <= 2:
            for k, v in erc721_dict[net_profits[i][0]].items():
                contract_addr = v['contract_address']
                break
            #imageURL = erc721_dict[net_profits[i][0]][[key for key in erc721_dict[net_profits[i][0]].keys()][0]]['image_url']
            token = [token for token in erc721_dict[net_profits[i][0]].keys()][0]
            imageURL = get_nft_image(contract_addr, token, ' ')
            leaderboard.append([net_profits[i][0], imageURL, '{:.3f}'.format(net_profits[i][1])])
        if net_profits[i][1] > 0:
            num_win_items += 1
        elif net_profits[i][1] < 0:
            num_loss_items += 1
    trade_info['Winning percentage'] = f'{num_win_items/(num_win_items+num_loss_items):.2%}'
    return trade_info, leaderboard

def frequent_trader(contract_addr, trader_num):
    print('Collecting frequently traders...')
    headers = {"Accept": 'application/json', "X-API-Key": 'BcK2Xcm8swRw7h7ogYx5dyL1XkiSnrZCqFDS2ki6cGUbgiOjvF1bkUedjb2QGqyW'}
    # contract_addr = ['0x60E4d786628Fea6478F785A6d7e704777c86a7c6', '0x1A92f7381B9F03921564a437210bB9396471050C', '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e', '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B']
    # contract_addr = ['0x60E4d786628Fea6478F785A6d7e704777c86a7c6', '0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e', '0x49cF6f5d44E70224e2E23fDcdd2C053F30aDA28B']
    url_list = ['https://deep-index.moralis.io/api/v2/nft/' +addr + '/transfers?chain=eth&format=decimal' for addr in contract_addr]
    tx_addr = []
    for url in tqdm(url_list):
        for pagenum in range(5):
            res = requests.get(url, headers=headers)
            res = json.loads(res.text)
            for i in range(len(res['result'])):
                from_addr = res['result'][i]['from_address']
                to_addr = res['result'][i]['to_address']
                tx_addr.append(from_addr)
                tx_addr.append(to_addr)
            cursor = res['cursor']
            res = requests.get(url, headers=headers)
            res = json.loads(res.text)
    data = Counter(tx_addr)
    data = data.most_common()
    frequent_trader_list = [data[i][0] for i in range(trader_num)]
    print('------------------------------')
    return frequent_trader_list

def frequent_trader_analysis(contract_addr, trader_num):
    frequent_trader_list = frequent_trader(contract_addr, trader_num)
    winRate_dict = {}
    trade_info_dict = {}
    for trader in tqdm(frequent_trader_list):
        try:
            erc721_transactions,all_transactions_dict, internal_transactions_dict,erc20_transactions_dict = get_tx_info(trader)
            erc721_dict = defaultdict(dict)
            get_buy_sell_history(erc721_dict, erc721_transactions,all_transactions_dict, internal_transactions_dict,erc20_transactions_dict,trader)
            get_opensea_floor_price(erc721_dict, trader)
            #get_history_transacted_images(erc721_dict)
            trade_info, leaderboard = calculat_cost_and_income(erc721_dict, trader)
            winRate_dict[trader] = trade_info['Winning percentage']
            trade_info_dict[trader] = trade_info
        except:
            continue
     
    # winRate_dict = OrderedDict(sorted(winRate_dict.items(), key=eval(operator.itemgetter(1)[:-1]), reverse=True))
    for k,v in winRate_dict.items():
        print(k)
        print('\tWinning percentage: {}'.format(trade_info_dict[k]['Winning percentage']))
        print('\tTotal profit: {}'.format(trade_info_dict[k]['Total profit']))
        print('------------------------------')
    return trade_info_dict
 
def get_transactions(WALLET_ADDRESS):
    erc721_transactions,all_transactions_dict, internal_transactions_dict,erc20_transactions_dict = get_tx_info(WALLET_ADDRESS)
    erc721_dict = defaultdict(dict)
    get_buy_sell_history(erc721_dict, erc721_transactions,all_transactions_dict, internal_transactions_dict,erc20_transactions_dict,WALLET_ADDRESS)
    get_opensea_floor_price(erc721_dict, WALLET_ADDRESS)
    get_history_transacted_images(erc721_dict)
    trade_info, leaderboard = calculat_cost_and_income(erc721_dict, WALLET_ADDRESS)
    return erc721_dict, trade_info, leaderboard

infura_url = 'https://mainnet.infura.io/v3/01883a27d4d54033933baa22cf45ead6'
web3 = Web3(Web3.HTTPProvider(infura_url))
app.run()
 
# frequent_trader_analysis(['0x60E4d786628Fea6478F785A6d7e704777c86a7c6'], 5)