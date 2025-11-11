import socket
import requests
import json
import threading
import time
import os
from datetime import datetime

class ChowdhuryVaiWHMTools:
    def __init__(self):
        self.version = "v2.0"
        self.author = "ChowdhuryVai"
        self.telegram_id = "https://t.me/darkvaiadmin"
        self.telegram_channel = "https://t.me/windowspremiumkey"
        self.website = "https://crackyworld.com/"
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        banner = f"""
\033[1;92m
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██████╗██╗  ██╗ ██████╗ ██╗    ██╗██╗   ██╗██████╗ ██╗   ██╗║
║ ██╔════╝██║  ██║██╔═══██╗██║    ██║██║   ██║██╔══██╗██║   ██║║
║ ██║     ███████║██║   ██║██║ █╗ ██║██║   ██║██████╔╝██║   ██║║
║ ██║     ██╔══██║██║   ██║██║███╗██║██║   ██║██╔══██╗██║   ██║║
║ ╚██████╗██║  ██║╚██████╔╝╚███╔███╔╝╚██████╔╝██║  ██║╚██████╔╝║
║  ╚═════╝╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ║
║                                                              ║
║              WHM/WHMCS Advanced Recon Tool                   ║
║                     {self.version} - {self.author}                 ║
║                                                              ║
║  Telegram: {self.telegram_id.split('/')[-1]:<25}           ║
║  Channel:  {self.telegram_channel.split('/')[-1]:<25}           ║
║  Website:  {self.website.split('//')[-1]:<25}           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
\033[0m
        """
        print(banner)
    
    def check_whm_access(self, domain, port=2087):
        """Check WHM access on standard and common ports"""
        print(f"\033[1;94m[*] Checking WHM access for: {domain}\033[0m")
        
        ports = [2087, 2083, 2086, 2095, 2082]
        results = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((domain, port))
                sock.close()
                
                if result == 0:
                    status = "\033[1;92mOPEN\033[0m"
                    results.append(f"Port {port}: {status} - WHM Access Possible")
                else:
                    status = "\033[1;91mCLOSED\033[0m"
                    results.append(f"Port {port}: {status}")
                    
            except Exception as e:
                results.append(f"Port {port}: \033[1;91mERROR\033[0m - {str(e)}")
        
        return results
    
    def find_hidden_paths(self, domain):
        """Find hidden WHM/WHMCS paths"""
        print(f"\033[1;94m[*] Scanning for hidden paths on: {domain}\033[0m")
        
        common_paths = [
            "/whm", "/cpanel", "/webmail", "/admin", "/administrator",
            "/whmcs", "/clientarea", "/adminarea", "/portal",
            "/cpanel/contact", "/cpanel/logout", "/cpanel/login",
            "/.well-known/", "/.git/", "/backup/", "/old/", "/test/",
            "/cpanel/logs", "/whm/logs", "/whmcs/admin"
        ]
        
        found_paths = []
        
        for path in common_paths:
            url = f"https://{domain}{path}"
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    found_paths.append(f"\033[1;92m[FOUND]\033[0m {url}")
                elif response.status_code == 403:
                    found_paths.append(f"\033[1;93m[FORBIDDEN]\033[0m {url}")
                elif response.status_code == 301 or response.status_code == 302:
                    found_paths.append(f"\033[1;96m[REDIRECT]\033[0m {url} -> {response.headers.get('Location')}")
            except:
                pass
        
        return found_paths
    
    def check_whmcs_info(self, domain):
        """Gather WHMCS information"""
        print(f"\033[1;94m[*] Gathering WHMCS information for: {domain}\033[0m")
        
        info = []
        whmcs_paths = [
            "/whmcs/", "/clientarea.php", "/cart.php", "/admin/",
            "/includes/", "/vendor/", "/modules/", "/attachments/"
        ]
        
        for path in whmcs_paths:
            url = f"https://{domain}{path}"
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    info.append(f"\033[1;92m[ACTIVE]\033[0m WHMCS Path: {path}")
                    if "WHMCS" in response.text:
                        info.append(f"\033[1;96m[INFO]\033[0m WHMCS detected at {path}")
            except:
                pass
        
        return info
    
    def subdomain_scan(self, domain):
        """Perform basic subdomain enumeration"""
        print(f"\033[1;94m[*] Scanning for subdomains: {domain}\033[0m")
        
        subdomains = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
            "ns2", "cpanel", "whm", "webmin", "admin", "blog", "shop", "forum", "demo",
            "test", "dev", "staging", "api", "secure", "portal", "host", "server"
        ]
        
        found_subs = []
        
        for sub in subdomains:
            url = f"https://{sub}.{domain}"
            try:
                response = requests.get(url, timeout=3, verify=False)
                if response.status_code == 200:
                    found_subs.append(f"\033[1;92m[LIVE]\033[0m {url}")
            except:
                pass
        
        return found_subs
    
    def server_info_scan(self, domain):
        """Gather server information"""
        print(f"\033[1;94m[*] Gathering server information: {domain}\033[0m")
        
        server_info = []
        
        try:
            ip = socket.gethostbyname(domain)
            server_info.append(f"\033[1;96m[IP]\033[0m {ip}")
            
            response = requests.get(f"https://{domain}", timeout=5, verify=False)
            headers = response.headers
            
            if 'Server' in headers:
                server_info.append(f"\033[1;96m[SERVER]\033[0m {headers['Server']}")
            if 'X-Powered-By' in headers:
                server_info.append(f"\033[1;96m[POWERED-BY]\033[0m {headers['X-Powered-By']}")
            if 'X-Panel' in headers:
                server_info.append(f"\033[1;92m[PANEL]\033[0m {headers['X-Panel']}")
                
        except Exception as e:
            server_info.append(f"\033[1;91m[ERROR]\033[0m Could not gather server info: {str(e)}")
        
        return server_info
    
    def comprehensive_scan(self, domain):
        """Perform comprehensive scan"""
        print(f"\033[1;95m[+] Starting comprehensive scan for: {domain}\033[0m")
        print("\033[1;95m[~] This may take a few moments...\033[0m")
        
        results = {
            'whm_ports': [],
            'hidden_paths': [],
            'whmcs_info': [],
            'subdomains': [],
            'server_info': []
        }
        
        threads = []
        
        def run_scan(scan_func, key, domain):
            results[key] = scan_func(domain)
        
        threads.append(threading.Thread(target=run_scan, args=(self.check_whm_access, 'whm_ports', domain)))
        threads.append(threading.Thread(target=run_scan, args=(self.find_hidden_paths, 'hidden_paths', domain)))
        threads.append(threading.Thread(target=run_scan, args=(self.check_whmcs_info, 'whmcs_info', domain)))
        threads.append(threading.Thread(target=run_scan, args=(self.subdomain_scan, 'subdomains', domain)))
        threads.append(threading.Thread(target=run_scan, args=(self.server_info_scan, 'server_info', domain)))
        
        for thread in threads:
            thread.start()
            time.sleep(0.1)
        
        for thread in threads:
            thread.join()
        
        return results
    
    def display_results(self, domain, results):
        """Display scan results in a formatted way"""
        print(f"\n\033[1;95m{'='*60}\033[0m")
        print(f"\033[1;95m SCAN RESULTS FOR: {domain}\033[0m")
        print(f"\033[1;95m{'='*60}\033[0m")
        
        print(f"\n\033[1;93m[WHM PORT SCAN]\033[0m")
        print(f"\033[1;93m{'-'*40}\033[0m")
        for result in results['whm_ports']:
            print(f"  {result}")
        
        print(f"\n\033[1;93m[SERVER INFORMATION]\033[0m")
        print(f"\033[1;93m{'-'*40}\033[0m")
        for info in results['server_info']:
            print(f"  {info}")
        
        print(f"\n\033[1;93m[HIDDEN PATHS]\033[0m")
        print(f"\033[1;93m{'-'*40}\033[0m")
        for path in results['hidden_paths']:
            print(f"  {path}")
        
        print(f"\n\033[1;93m[WHMCS INFORMATION]\033[0m")
        print(f"\033[1;93m{'-'*40}\033[0m")
        for info in results['whmcs_info']:
            print(f"  {info}")
        
        print(f"\n\033[1;93m[SUBDOMAINS]\033[0m")
        print(f"\033[1;93m{'-'*40}\033[0m")
        for sub in results['subdomains']:
            print(f"  {sub}")
        
        print(f"\n\033[1;95m{'='*60}\033[0m")
        print(f"\033[1;92m Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print(f"\033[1;95m{'='*60}\033[0m")
    
    def save_results(self, domain, results):
        """Save results to file"""
        filename = f"scan_results_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Scan Results for: {domain}\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tool: ChowdhuryVai WHM Tools {self.version}\n")
            f.write("="*50 + "\n\n")
            
            f.write("WHM PORT SCAN:\n")
            f.write("-"*20 + "\n")
            for result in results['whm_ports']:
                clean_result = result.replace('\033[1;92m', '').replace('\033[1;91m', '').replace('\033[1;93m', '').replace('\033[1;96m', '').replace('\033[0m', '')
                f.write(clean_result + "\n")
            
            f.write("\nSERVER INFORMATION:\n")
            f.write("-"*20 + "\n")
            for info in results['server_info']:
                clean_info = info.replace('\033[1;92m', '').replace('\033[1;91m', '').replace('\033[1;93m', '').replace('\033[1;96m', '').replace('\033[0m', '')
                f.write(clean_info + "\n")
            
            f.write("\nHIDDEN PATHS:\n")
            f.write("-"*20 + "\n")
            for path in results['hidden_paths']:
                clean_path = path.replace('\033[1;92m', '').replace('\033[1;91m', '').replace('\033[1;93m', '').replace('\033[1;96m', '').replace('\033[0m', '')
                f.write(clean_path + "\n")
            
            f.write("\nWHMCS INFORMATION:\n")
            f.write("-"*20 + "\n")
            for info in results['whmcs_info']:
                clean_info = info.replace('\033[1;92m', '').replace('\033[1;91m', '').replace('\033[1;93m', '').replace('\033[1;96m', '').replace('\033[0m', '')
                f.write(clean_info + "\n")
            
            f.write("\nSUBDOMAINS:\n")
            f.write("-"*20 + "\n")
            for sub in results['subdomains']:
                clean_sub = sub.replace('\033[1;92m', '').replace('\033[1;91m', '').replace('\033[1;93m', '').replace('\033[1;96m', '').replace('\033[0m', '')
                f.write(clean_sub + "\n")
        
        print(f"\033[1;92m[+] Results saved to: {filename}\033[0m")
    
    def run(self):
        """Main application runner"""
        self.clear_screen()
        self.print_banner()
        
        while True:
            print("\n\033[1;96m[MAIN MENU]\033[0m")
            print("\033[1;96m1. Quick WHM Port Scan\033[0m")
            print("\033[1;96m2. Hidden Path Scanner\033[0m")
            print("\033[1;96m3. WHMCS Information Gatherer\033[0m")
            print("\033[1;96m4. Subdomain Scanner\033[0m")
            print("\033[1;96m5. Comprehensive Scan\033[0m")
            print("\033[1;96m6. Server Information\033[0m")
            print("\033[1;91m7. Exit\033[0m")
            
            choice = input("\n\033[1;93mChoose an option (1-7): \033[0m")
            
            if choice == '1':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.check_whm_access(domain)
                print(f"\n\033[1;95mWHM Port Scan Results for {domain}:\033[0m")
                for result in results:
                    print(f"  {result}")
                    
            elif choice == '2':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.find_hidden_paths(domain)
                print(f"\n\033[1;95mHidden Paths Found for {domain}:\033[0m")
                for path in results:
                    print(f"  {path}")
                    
            elif choice == '3':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.check_whmcs_info(domain)
                print(f"\n\033[1;95mWHMCS Information for {domain}:\033[0m")
                for info in results:
                    print(f"  {info}")
                    
            elif choice == '4':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.subdomain_scan(domain)
                print(f"\n\033[1;95mSubdomains Found for {domain}:\033[0m")
                for sub in results:
                    print(f"  {sub}")
                    
            elif choice == '5':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.comprehensive_scan(domain)
                self.display_results(domain, results)
                save = input("\n\033[1;93mSave results to file? (y/n): \033[0m")
                if save.lower() == 'y':
                    self.save_results(domain, results)
                    
            elif choice == '6':
                domain = input("\n\033[1;93mEnter domain: \033[0m")
                results = self.server_info_scan(domain)
                print(f"\n\033[1;95mServer Information for {domain}:\033[0m")
                for info in results:
                    print(f"  {info}")
                    
            elif choice == '7':
                print("\n\033[1;92mThank you for using ChowdhuryVai WHM Tools!\033[0m")
                print(f"\033[1;94mTelegram: {self.telegram_id}\033[0m")
                print(f"\033[1;94mChannel: {self.telegram_channel}\033[0m")
                print(f"\033[1;94mWebsite: {self.website}\033[0m")
                break
                
            else:
                print("\n\033[1;91mInvalid choice! Please try again.\033[0m")
            
            input("\n\033[1;93mPress Enter to continue...\033[0m")
            self.clear_screen()
            self.print_banner()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    try:
        tool = ChowdhuryVaiWHMTools()
        tool.run()
    except KeyboardInterrupt:
        print("\n\033[1;91mTool interrupted by user. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[1;91mAn error occurred: {str(e)}\033[0m")
