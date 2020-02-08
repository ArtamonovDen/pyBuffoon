import click
from os import listdir, getcwd
from os.path import isfile, join, isabs
from PyPDF2 import PdfFileMerger

@click.command()
@click.argument('inputs', nargs=-1,type=click.Path(exists=True, readable=True))
@click.option('-o', '--output', default='./merged.pdf', help='Path to merged pdf-file')
@click.option('-d','--dir', type=click.Path(exists=True, dir_okay=True))
def parse_args(inputs, output, dir):
    if dir:
        path = join(getcwd(), dir) if not isabs(dir) else dir
        inputs = [join(path, f) for f in listdir(path) 
            if isfile(join(path, f)) and join(path, f).endswith('.pdf')]

    try:
        merge(inputs, output)  
    except Exception as e:
        click.echo(click.style(f'Some errors occured: {e}', fg='red'))
    else:
        click.echo(click.style(f'Merged into {output}', fg='green'))

   

def merge(inputs, output):
    '''
        Merge input pdf-files
    '''    
    if not output.endswith('.pdf'):
        raise Exception('Wrong output file name')
    out = open(output, 'wb') 
    merger = PdfFileMerger()
    for input in inputs:
        inp = open(input,'rb')
        merger.append(fileobj=inp)    
    merger.write(out)
    out.close()
    merger.close()


if __name__=='__main__':
    parse_args()

