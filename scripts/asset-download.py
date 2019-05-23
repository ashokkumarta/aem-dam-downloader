import os, requests, json, time
from datetime import datetime
from log_util import * 

def load_config():
    config_file = 'config/config.json'
    config=open(config_file).read()
    return json.loads(config)

def getTargetPath(asset):
    target_full_path = config_json['path_to_download'] + asset
    return os.path.dirname(target_full_path), os.path.basename(target_full_path)

def logStatus(msg):
    s_log.info(msg)
    print (msg)

def get_timestamp():
    return datetime.now().strftime('%d %b %Y, %H:%M:%S')

# Start 
s_time = get_timestamp()


#Load config
config_json = load_config()

# Initialize loggers
t_log = get_logger(config_json['trace_log'])
e_log = get_logger(config_json['error_log'])
s_log = get_output_handler(config_json['status_log'])

# Initialize output file handler (uses log library)
s_handle = get_output_handler(config_json['successful_assets'])
f_handle = get_output_handler(config_json['failed_assets'])

# Initialize variables
assets_to_download = []
total = 0
failure = 0

try:

    session = requests.Session()
    session.auth = (config_json['cq_user'], config_json['cq_password'])
    session.post(config_json['cq_protocal']+'://'+config_json['cq_host']+':'+config_json['cq_port'])

    for dam_path in config_json['base_paths']:

        #Form URL to fetch metadata for the given path
        url = config_json['cq_protocal']+'://'+config_json['cq_host']+':'+config_json['cq_port']+'/bin/querybuilder.json?type=dam:Asset&path='+dam_path+'&p.limit=-1&p.hits=selective&p.properties='+' '.join(config_json['extract_properties'])+'&p.nodedepth=-1'

        #Fetch metadata
        t_log.info('Fetching metadata of all assets for processing')

        response = session.get(url).content
        t_log.info(response)

        #Parse metadata to identify all assets
        t_log.info('Parsing asset metadata...')
        data = json.loads(response)

        # Accumulate all assets to be downloaded
        for asset in data[config_json['asset_json_node']]:
            assets_to_download.append(asset[config_json['path_json_node']].encode('utf-8'))

    # For each asset to download
    for aset in assets_to_download:
        
        total += 1
        
        t_log.info("Asset : "+str(total) + ' of ' + str(len(assets_to_download)))

        try:
            
            # Decode / Encode & form URL
            asset = aset.decode('utf-8')
            url_path = config_json['cq_protocal']+'://'+config_json['cq_user']+':'+config_json['cq_password']+'@'+config_json['cq_host']+':'+config_json['cq_port']+asset
            url_path = url_path.encode('utf-8')

            # Fetch asset
            result = session.get(url_path)

            # Success
            if 200 == result.status_code:
                try:
                    dir, name = getTargetPath(asset)
                    if not os.path.isdir(dir):
                        os.makedirs(dir)
                    f_out = open(dir+'/'+name, 'wb')
                    f_out.write(result.content)
                    f_out.close()
                    s_handle.info(asset)
                    t_log.info("Downloaded asset : "+asset)
                except  Exception as e:
                    e_log.error('Unexpected error in fetching and storing asset : '+str(asset))
                    e_log.error('Exception : '+str(e))
                    failure += 1
                    f_handle.info(asset)
            # Failure
            else:
                e_log.error('Unable to download asset : '+str(asset))
                e_log.error('Status code : '+str(result.getcode()))
                failure += 1
                f_handle.info(asset)

        except  Exception as e:
            e_log.error('Unexpected Error in downloading asset : '+str(asset))
            e_log.error('Exception : '+str(e))
            failure += 1
            f_handle.info(asset)

        # Wait before the next download
        time.sleep(config_json["time_wait_secs"])
                
except  Exception as e:
    e_log.error('Unexpected Error : '+str(e))


# Report status
logStatus("\nStatus:\n=======")
logStatus("Download start time : "+s_time)
logStatus("Download completion time : "+get_timestamp())
logStatus("Assets downloaded : "+str(total - (failure)))
if failure :
    logStatus("Download failed : "+str(failure))
    logStatus("Check the logs at "+config_json['error_log']+" for error details")

