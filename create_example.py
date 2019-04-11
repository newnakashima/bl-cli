import configparser

config = configparser.ConfigParser()

print("Please input your backlog url: ")
base_url = input()
print("Please input your backlog access key: ")
access_key = input()

config['nksm'] = {
    'base_url':base_url,
    'access_key': access_key,
}
with open('example.ini', 'w') as configfile:
    config.write(configfile)
