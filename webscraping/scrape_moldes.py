"""
Module to scrape unique ID_MOLDE data from Bricklink.
Fetches name, weight, and raw name for category extraction.
"""
import requests
from bs4 import BeautifulSoup
import time
import random


def scrape_molde_data(id_molde, headers=None):
    """
    Scrape data for a single ID_MOLDE from Bricklink.
    
    Args:
        id_molde (str): The piece ID to scrape
        headers (dict): Optional HTTP headers for the request
    
    Returns:
        dict: Dictionary with keys 'id_molde', 'name', 'weight', or None if failed
    """
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}
    
    url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={id_molde}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"⚠️  Error {response.status_code} al acceder ID_MOLDE: {id_molde}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract piece name
        title_tag = soup.find("h1", {"id": "item-name-title"})
        piece_name = title_tag.text.strip() if title_tag else "N/A"
        
        # Extract weight
        weight_tag = soup.find("span", {"id": "item-weight-info"})
        weight = weight_tag.text.strip() if weight_tag else "N/A"
        
        return {
            "id_molde": id_molde,
            "name": piece_name,
            "weight": weight
        }
    
    except requests.RequestException as e:
        print(f"⚠️  Request error para ID_MOLDE {id_molde}: {e}")
        return None
    except Exception as e:
        print(f"⚠️  Error inesperado para ID_MOLDE {id_molde}: {e}")
        return None


def scrape_multiple_moldes(id_moldes, delay_range=(1.5, 2.5)):
    """
    Scrape data for multiple unique ID_MOLDEs with rate limiting.
    
    Args:
        id_moldes (list): List of unique ID_MOLDE strings
        delay_range (tuple): Min and max delay in seconds between requests
    
    Returns:
        dict: Dictionary mapping id_molde -> {name, weight}
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    molde_data = {}
    total = len(id_moldes)
    
    print(f"\n🔍 Iniciando scraping de {total} ID_MOLDEs únicos...")
    print("=" * 60)
    
    for idx, id_molde in enumerate(id_moldes, 1):
        data = scrape_molde_data(id_molde, headers)
        
        if data:
            molde_data[id_molde] = {
                "name": data["name"],
                "weight": data["weight"]
            }
            print(f"✓ [{idx}/{total}] {id_molde}: {data['name'][:50]}...")
        else:
            # Store N/A for failed scrapes
            molde_data[id_molde] = {
                "name": "N/A",
                "weight": "N/A"
            }
            print(f"✗ [{idx}/{total}] {id_molde}: FAILED")
        
        # Rate limiting - skip delay on last item
        if idx < total:
            delay = delay_range[0] + random.random() * (delay_range[1] - delay_range[0])
            time.sleep(delay)
    
    print("=" * 60)
    print(f"✓ Scraping completado: {len([d for d in molde_data.values() if d['name'] != 'N/A'])}/{total} exitosos\n")
    
    return molde_data
