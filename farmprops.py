import re, os, urllib, time, json

def parse_properties(pfile):
    result = {}
    re_prog = re.compile('(file:[/]+|http:[/]+)?([$]{1}[{]{1}([0-9a-zA-Z.]+)[}]{1})')
    for line in pfile.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue
        else:
            kv = line.split('=')
            re_match = re_prog.match(kv[1])
            if bool(re_match):
                kv[1] = kv[1].replace(re_match.group(2), result[re_match.group(3)])
            result[kv[0]] = kv[1]

    return result


def write_jobfarm_config_files(props):
    def write_config_file(file, match):
        for prop in [x for x in props.keys() if x.split('.')[0] == match]:
            file.write("%s=%s\n" % (prop, props[prop]))
        file.close
        
    agent = open("%s/config/jobfarm.agent.properties" % (props['jf.target.path']), "w")
    mothership = open("%s/config/mothership.properties" % (props['jf.target.path']), "w")

    write_config_file(agent, 'agent')
    write_config_file(mothership, 'mothership')

def retrieve_jobfarm_core_config(props):
    uo = urllib.URLopener()
    url = props['mothership.core.url']
    uo.retrieve(url, "%s/config/core/%s.json" % (props['jf.target.path'], \
                                                 props['mothership.core.url'].split('/')[-1]))
    

# parse configuration file
#f = open("/../../../../../../users/bbuckey/projects/pythonprogs/deploy.properties", 'r')
f = open("depoly.properties", 'r')

props = parse_properties(f)

#check out jobfarm project
#checkout_jobfarm(props)
#build_jobfarm(props)
#deploy_jobfarm(props)
write_jobfarm_config_files(props)
retrieve_jobfarm_core_config(props)

#launch_jobfarm(props)
