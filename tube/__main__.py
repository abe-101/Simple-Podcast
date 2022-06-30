import sys
import os
import click
import getpass

from validate_id import valid_id
from my_scrapetube import return_channel, return_playlist
from youtube_to_anchorFM import convert_youtube_to_podcast

@click.group()
@click.option("-d", "--draft-mode", is_flag=True, help="Save podcast as draft")
@click.option('-t', '--thumbnail_mode', is_flag=True, help="Include YouTube thumbnail in podcast")
@click.option('-u', '--add-url', is_flag=True, help="Add the YouTube URL To podcast description")
@click.option('-x', '--is-explicit', is_flag=True, help="Mark podcast as explicit")
@click.pass_context
def cli(ctx, draft_mode, thumbnail_mode, add_url, is_explicit):
    """Convert YouTube video(s) to Anchor FM"""
    ctx.ensure_object(dict)

    ctx.obj['draft_mode'] = draft_mode
    ctx.obj['thumbnail_mode'] = thumbnail_mode
    ctx.obj['url_in_description'] = add_url
    ctx.obj['is_explicit'] = is_explicit

    if not os.getenv("ANCHOR_EMAIL") or not os.getenv("ANCHOR_PASSWORD"):
        os.environ["ANCHOR_EMAIL"] = input("Enter anchor.FM user email: ")
        os.environ["ANCHOR_PASSWORD"] = getpass.getpass("Enter anchor.FM password: ")
    pass

@cli.command()
@click.pass_context
@click.argument('ids', nargs=-1)
def youtube_id(ctx, ids):
    """Takes in YouTube ID(s) as arguments"""
    click.echo(f'Converting Youtube Video to Anchor FM')
    ids = list(ids)
    convert_youtube_to_podcast(ids, **ctx.obj)

@cli.command()
@click.pass_context
@click.argument('filename', type=click.Path(exists=True))
def youtube_id_from_file(ctx, filename):
    """Takes in a file containing youtube id (one per line)"""
    click.echo(f'Converting Youtube Video (from file) to Anchor FM')
    ids = []
    with open(filename) as file:
        for row in file:
            ids.append(row.rstrip("\n"))

    convert_youtube_to_podcast(ids, **ctx.obj)

@cli.command()
@click.pass_context
@click.argument('channel-id')
def youtube_channel(ctx, channel_id):
    """Takes in a YouTube Channel ID"""
    click.echo('Converting YouTube Channel to Anchor FM')
    channel_vids = return_channel(channel_id)
    convert_youtube_to_podcast(channel_vids, **ctx.obj)


@cli.command()
@click.pass_context
def youtube_playlist(ctx, playlist_id):
    """Take in a YouTube Playlist ID"""
    click.echo('Converting YouTube Playlist to Anchor FM')
    playlist_vids = return_playlist(playlist_id)
    convert_youtube_to_podcast(playlist_vids, **ctx.obj)

if __name__ == '__main__':
    cli()
