from devkit.utils.shell import exec_capture

def fzf_select(items: list[str], prompt: str = 'Select > ') -> str:
    '''Pipe items through fzf and return selected line.'''
    proc = exec_capture(
        ['fzf', f'--prompt={prompt}', '--height=40%', '--border'],
        input='\n'.join(items)
    )
    return proc.strip()
