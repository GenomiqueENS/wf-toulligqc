
def is_metadata(key):   
    metadata = ['sequencing.telemetry.extractor.flowcell.id',
    'sequencing.telemetry.extractor.run.id',
    'sequencing.telemetry.extractor.sample.id',
    'sequencing.telemetry.extractor.minknow.version',
    'sequencing.telemetry.extractor.device.id',
    'sequencing.telemetry.extractor.device.type',
    'sequencing.telemetry.extractor.distribution.version',
    'sequencing.telemetry.extractor.flow.cell.product.code',
    'sequencing.telemetry.extractor.software.name',
    'sequencing.telemetry.extractor.software.version',
    'sequencing.telemetry.extractor.kit.version',
    'sequencing.telemetry.extractor.flowcell.version']
    return True if key in metadata else False


def check_metadata(data):
    sample_details = {}
    with open(data) as f:
        for line in f:
            (key, val) = line.split('=')
            if is_metadata(key):
                key = ' '.join(key.split('.')[3:]).capitalize()
                sample_details[key] = val
    return sample_details

