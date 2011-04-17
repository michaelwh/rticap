import functools
import PySide

def qtLink(source, signal, target, *args, **kwargs) :
    """TAKEN FROM: http://talk.maemo.org/showthread.php?t=60687
    
    allows us to get around the problem that eg clicked signals in
    pyside can't send parameters
    
    example usage:
        pysideutil.qtLink(modeButton, "clicked()", self.currentModeChangedCallback, guiMode)""" 
    proxy_target = functools.partial(target, *args, **kwargs)
    source.connect(source, PySide.QtCore.SIGNAL(signal), proxy_target)