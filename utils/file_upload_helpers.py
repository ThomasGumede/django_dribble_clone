def upload_shotfiles_hook(instance, filename):
    return F"shot/files-{instance.shot.id}/{filename}"

def upload_shotcover_hook(instance, filename):
    return F"shot/files-{instance.id}/{filename}"