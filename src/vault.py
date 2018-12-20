#!/usr/bin/env python

import re
import sys
import os
import logging
import argparse
import logger
import colors
from urllib.parse import urlparse
import dorker

def check_url(url: str):
    """Check whether or not URL have a scheme

        :url: URL that is to be checked
    """
    if not urlparse(url).scheme:
        return 'http://' + url

    return url

def check_ip(ip: str):
    """
    Check whether the input IP is valid or not
    """
    if re.match(r'^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(\.(?!$)|$)){4}$', ip):
        return ip
    else:
        colors.error('Please enter a valid IP address')
        LOGGER.error('[-] Please enter a valid IP address')
        sys.exit(1)

def ssl(args):
    if not args.url:
        colors.error('Please enter an URL for SSL scanning')
        LOGGER.error('[-] Please enter an URL for SSL scanning')
        sys.exit(1)
    try:
        from lib.ssl_scanner import ssl_scanner
        colors.info('SSL scan using SSL Labs API')

        data = ssl_scanner.analyze(args.url)
        ssl_data = ssl_scanner.vulnerability_parser(data)

        if args.output:
            if args.output.endswith('.txt'):
                file = args.output
            else:
                file = args.output + '.txt'

            with open(file, 'wt') as f:
                f.write('[+] Vulnerability Scan Result : \n\n')
                for k, v in ssl_data.items():
                    f.write(str(k) + ' : ' + str(v) + os.linesep)

            colors.success('File has been saved successfully')

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def info(args):
    if not args.url:
        colors.error('Please enter an URl for information gathering')
        LOGGER.error('[-] Please enter an URl for information gathering')
        sys.exit(1)
    try:
        from lib.info_gathering import header_vuln
        colors.info('Performing information gathering over : {}'.format(args.url))

        infoGatherObj = header_vuln.HeaderVuln(args.url)
        header_data = infoGatherObj.gather_header()
        cookie_data = infoGatherObj.insecure_cookies()
        method_data = infoGatherObj.test_http_methods()

        if args.output:
            if args.output.endswith('.txt'):
                file = args.output
            else:
                file = args.output + '.txt'
            i = 1

            with open(file, 'w') as f:
                f.write('---[!] Header Details---\n\n')

                for k, v in header_data.items():
                    f.write(str(k) + ' : ' + str(v) + os.linesep)
                f.write('\n---[!] Testing Insecure Cookies---\n\n')

                for k in cookie_data:
                    f.write(k + os.linesep)
                f.write('\n---[!] Testing HTTP methods---\n\n')

                for k in method_data:
                    if i % 3 != 0:
                        f.write(str(k) + ' ')
                    else:
                        f.write(str(k) + os.linesep)
                    i = i + 1

            colors.success('File has been saved successfully')

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def comment(args):
    if not args.url:
        colors.error('Please enter an URL for finding comments')
        LOGGER.error('[-] Please enter an URL for finding comments')
        sys.exit(1)
    try:
        from lib.info_gathering import finding_comment
        colors.info('Performing comment gathering over : {}'.format(args.url))

        findCommnentObj = finding_comment.FindingComments(args.url)
        comment_dict = findCommnentObj.parse_comments()

        if args.output:
            if args.output.endswith('.txt'):
                file = args.output
            else:
                file = args.output + '.txt'

            with open(file, 'w') as f:
                f.write('---[!] Comments---\n\n')
                for k, v in comment_dict.items():
                    f.write(str(k) + ' : ' + str(v) + os.linesep)
            colors.success('File has been saved successfully')

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def fuzz(args):
    if not args.url:
        colors.error('Please enter an URL for fuzzing')
        LOGGER.error('[-] Please enter an URL for fuzzing')
        sys.exit(1)
    try:
        from lib.fuzzer import fuzzer
        colors.info('Performing fuzzing on : {}'.format(args.url))
        fuzzObj = fuzzer.Fuzzer(base_url=args.url, thread_num=args.threads)
        fuzzObj.initiate()

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def fin(args):
    if not args.ip:
        colors.error('Please enter an IP address for scanning')
        LOGGER.error('[-] Please enter an IP address for scanning')
        sys.exit(1)
    try:
        colors.info('Initiating FIN Scan')

        from lib.port_scanner import port_scanner

        portScanObj = port_scanner.PortScanner(ip=args.ip, start_port=args.start_port,
                                               end_port=args.end_port, threads=args.threads,
                                               source_port=args.source_port)
        portScanObj.fin_scan()
    except ImportError:
        colors.error('Could not import the required module')
        LOGGER.error('[-] Could not import the required module')
        sys.exit(1)
    except Exception as e:
        LOGGER.error(e)

def null(args):
    if not args.ip:
        colors.error('Please enter an IP address for scanning')
        LOGGER.error('[-] Please enter an IP address for scanning')
        sys.exit(1)
    try:
        colors.info('Initiating NULL Scan')

        from lib.port_scanner import port_scanner

        portScanObj = port_scanner.PortScanner(ip=args.ip, start_port=args.start_port,
                                               end_port=args.end_port, threads=args.threads,
                                               source_port=args.source_port)
        portScanObj.null_scan()
    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
        sys.exit(1)
    except Exception as e:
        LOGGER.error(e)

def ack(args):
    if not args.ip:
        colors.error('Please enter an IP address for scanning')
        LOGGER.error('[-] Please enter an IP address for scanning')
        sys.exit(1)
    try:
        colors.info('Initiating TCP ACK Scan')

        from lib.port_scanner import port_scanner

        portScanObj = port_scanner.PortScanner(ip=args.ip, start_port=args.start_port,
                                               end_port=args.end_port, threads=args.threads,
                                               source_port=args.source_port)
        portScanObj.tcp_ack_scan()
    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def whois(args):
    if not args.ip:
        colors.error('Please enter an IP for Whois lookup')
        LOGGER.error('[-] Please enter an IP for Whois lookup')
        sys.exit(1)
    try:
        from lib.whois_lookup import lookup
        data = lookup.whois_lookup(args.ip)

        colors.success('Information after Whois lookup: \n')

        for k, v in data.items():
            print(k, ':', v)

        if args.output:
            if args.output.endswith('.txt'):
                file = args.output
            else:
                file = args.output + '.txt'

            with open(file, 'w') as f:
                f.write('Information after Whois lookup: \n\n')
                for k, v in data.items():
                    f.write(str(k) + ' : ' + str(v) + os.linesep)
            colors.success('File has been saved successfully')

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
    except Exception as e:
        LOGGER.error(e)

def lfi(args):
    if not args.url:
        colors.error('Please enter an URL  for scanning')
        LOGGER.error('[-] Please enter an URL for scanning')
        sys.exit(1)
    try:
        colors.info('Initiating LFI Scan')

        from lib.website_scanner.lfi import lfiEngine
        lfiscanObj = lfiEngine.LFI(url=args.url, payload_path=os.getcwd() + '/payloads/lfi_payloads.json')
        lfiscanObj.startScanner()

    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
        sys.exit(1)
    except Exception as e:
        LOGGER.error(e)

def dork(args):

    if args.dork:
        dorks = args.dork
        page = int(input("\nNumber of Pages to scrap :: \033[1;37m"))
        print('\n\033[1;37m[>]Searching ...\033[1;37m  \n')
        web_lists = dorker.start_dorking(dorks, page)

        if args.output:
            if args.output.endswith('.txt'):
                file = args.output
            else:
                file = args.output + '.txt'

            with open(file, 'w') as f:
                f.write('Google Dorks results: \n\n')
                for k in web_lists:
                    f.write(str(k) + os.linesep)
            colors.success('File has been saved successfully')

def xmas(args):
    if not args.ip:
        colors.error('Please enter an IP address for scanning')
        LOGGER.error('[-] Please enter an IP address for scanning')
        sys.exit(1)
    try:
        colors.info('Initiating XMAS Scan')

        from lib.port_scanner import port_scanner

        portScanObj = port_scanner.PortScanner(ip=args.ip, start_port=args.start_port,
                                               end_port=args.end_port, threads=args.threads,
                                               source_port=args.source_port)
        portScanObj.xmas_scan()
    except ImportError:
        colors.error('Could not import the required module.')
        LOGGER.error('[-] Could not import the required module.')
        sys.exit(1)
    except Exception as e:
        LOGGER.error(e)

def ping_sweep(args):
    if not args.ip:
        colors.error('Please enter an IP address for scanning')
        sys.exit(1)
    else:
        try:
            colors.info('Initiating Ping Sweep Scan')

            from lib.ip_scanner import ping_sweep

            pingSweepObj = ping_sweep.IPScanner(ip=args.ip,
                                                start_ip=args.ip_start_range,
                                                end_ip=args.ip_end_range,
                                                threads=args.threads)
            pingSweepObj.threadingScan()
        except ImportError:
            colors.error('Could not import the required module.')
        except Exception as e:
            print(e)

def xss(args):
    if args.url:
        links = []

        path = os.getcwd() + '/lib/website_scanner/xss'
        sys.path.insert(0, path)

        if args.this:
            colors.success('Performing XSS Vulnerability Scan on : {}'.format(args.url))
            links.append(args.url)
        else:
            colors.success('Collecting all the links, crawling : {}'.format(args.url))

            try:
                import crawler
                crawlObj = crawler.Crawl(url=args.url)
                links = crawlObj.getList()
            except ImportError:
                colors.error('Could not import the required module.')
                LOGGER.error('[-] Could not import the required module.')
            except Exception as e:
                LOGGER.error(e)
                
        try:
            import xss

            xssScanObj = xss.XSS(url=links,
                                 payload_file=os.getcwd() + '/payloads/xss_payloads.txt')
            xssScanObj.initiateEngine()
        except ImportError:
            colors.error('Could not import the required module')
            LOGGER.error('[-] Could not import the required module')
            sys.exit(1)
        except Exception as e:
            LOGGER.error(e)
    else:
        colors.error('Please enter an URL for XSS Scanning')
        LOGGER.error('[-] Please enter an URL for XSS Scanning')
        sys.exit(1)

def ddos(args):
    if args.url is None and args.ip is None:
        colors.error('Please provide either an IP address or an URL to perform DDoS attack')
        sys.exit(1)
    else:
        try:
            from lib.ddos import ddos

            ddosObj = ddos.DDoS(url=args.url, ip=args.ip, start_port=args.start_port,
                                end_port=args.end_port, dport=args.port,
                                threads=args.threads, interval=args.interval)
            ddosObj.startAttack()
        except ImportError:
            colors.error('Could not import the required module')
            LOGGER.error('[-] Could not import the required module')
        except Exception as e:
            print(e)
            LOGGER.error(e)
            sys.exit(1)
            
def dorking():
    dorks=args.dork
    page=int(input("\nNumber of Pages to scrap :: \033[1;37m"))
    print('\n\033[1;37m[>]Searching ...\033[1;37m  \n')
    dorker.start_dorking(dorks,page)

if __name__ == '__main__':

    print(""" ____   _________   ____ ___.____  ___________
\   \ /   /  _  \ |    |   \    | \__    ___/
 \   Y   /  /_\  \|    |   /    |   |    |
  \     /    |    \    |  /|    |___|    |
   \___/\____|__  /______/ |_______ \____|
                \/                 \/         """)

    print("\nWelcome to Vault...!\n")

    log_file_name = os.path.join(os.getcwd(), "vault.log")
    logger.Logger.create_logger(log_file_name, __package__)
    LOGGER = logging.getLogger(__name__)

    # Taking in arguments
    parser = argparse.ArgumentParser(description="VAULT")

    parser.add_argument('-u', '--url', help='URL for scanning')
    parser.add_argument('-p', '--port', help='Single port for scanning')
    parser.add_argument('-sp', '--start_port', help='Start port for scanning')
    parser.add_argument('-ep', '--end_port', help='End port for scanning')
    parser.add_argument('-ssl', action='store_true', help='perform SSL scan')
    parser.add_argument('-info', action='store_true', help='Gather information')
    parser.add_argument('-comment', action='store_true', help='Finding comments')
    parser.add_argument('-fuzz', action='store_true', help='Fuzzing URL')
    parser.add_argument('-ip', '--ip', help='IP address for port scanning')
    parser.add_argument('-t', '--threads', help='Number of threads to use')
    parser.add_argument('-source_port', help='Source port for sending packets')
    parser.add_argument('-fin', action='store_true', help='Perform FIN Scan')
    parser.add_argument('-null', action='store_true', help='Perform NULL Scan')
    parser.add_argument('-ack', action='store_true', help='Perform TCP ACK Scan')
    parser.add_argument('-xmas', action='store_true', help='Perform XMAS Scan')
    parser.add_argument('-c', '--crawl', action='store_true', help='Crawl and collect all the links')
    parser.add_argument('-xss', action='store_true', help='Scan for XSS vulnerabilities')
    parser.add_argument('-this', action='store_true', help='Only scan the given URL, do not crawl')
    parser.add_argument('-ping_sweep', action='store_true', help='ICMP ECHO request')
    parser.add_argument('-ip_start_range', help='Start range for scanning IP')
    parser.add_argument('-ip_end_range', help='End range for scanning IP')
    parser.add_argument('-lfi', action='store_true', help='Scan for LFI vulnerabilities')
    parser.add_argument('-whois', action='store_true', help='perform a whois lookup of a given IP')
    parser.add_argument('-o', '--output', help='Output all data')
    parser.add_argument('-d', '--dork', help='Perform google dorking')
    parser.add_argument('-ddos', action='store_true', help='Perform DDoS attack')
    parser.add_argument('-interval', help='Interval time for sending packets')
    parser.add_argument('-all', action='store_true', help='Run all scans')

    colors.info("Please Check log file for information about any errors")

    # Print help message if no arguments are supplied
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()

    if args.all:
        if args.url:
            args.url = check_url(args.url)
            ssl(args)
            info(args)
            fuzz(args)
            comment(args)
            xss(args)
            lfi(args)

        if args.ip:
            args.ip = check_ip(args.ip)
            whois(args)
            xmas(args)
            fin(args)
            null(args)
            ack(args)
            ping_sweep(args)

    if args.url:
        args.url = check_url(args.url)

    if args.ip:
        args.ip = check_ip(args.ip)

    if args.port:
        args.start_port = args.port
        args.end_port = args.port

    if args.whois:
        whois(args)

    if args.ssl:
        ssl(args)

    if args.info:
        info(args)

    if args.fuzz:
        fuzz(args)

    if args.comment:
        comment(args)

    if args.fin:
        fin(args)

    if args.null:
        null(args)

    if args.ack:
        ack(args)

    if args.xmas:
        xmas(args)

    if args.xss:
        xss(args)

    if args.ping_sweep:
        ping_sweep(args)

    if args.lfi:
        lfi(args)

    if args.ddos:
        ddos(args)

    if args.dork:
        dork(args)
