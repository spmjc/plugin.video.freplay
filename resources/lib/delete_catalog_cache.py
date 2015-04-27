#-*- coding: utf-8 -*-
import globalvar
import shutil
import xbmcgui

def delete_catalog_cache() :
    if os.path.exists(globalvar.CACHE_DIR) :
        shutil.rmtree(globalvar.CACHE_DIR)
    if not os.path.exists(globalvar.CACHE_DIR):
        os.makedirs(globalvar.CACHE_DIR, mode=0777)
    xbmcgui.Dialog().ok(globalvar.LANGUAGE(30000), globalvar.LANGUAGE(32000))
    
if ( __name__ == "__main__" ):
    if  globalvar.CACHE_DIR != '' :
        delete_catalog_cache()
