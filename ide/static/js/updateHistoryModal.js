import React from 'react';

class UpdateHistoryModal extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let data = [];

    Object.keys(this.props.modelHistory).sort().reverse().forEach((versionId, index) => {
      let url = 'http://localhost:8000/load?id=' + this.props.networkId + '&version=' + versionId;
      let msg = '';

      if(this.props.modelHistory[versionId] == 'AddComment') {
        msg = 'Add a comment on layer';
      }
      else if(this.props.modelHistory[versionId] == 'AddLayer') {
        msg = 'New layer added';
      }
      else if(this.props.modelHistory[versionId] == 'DeleteLayer') {
        msg = 'Deleted existing layer';
      }
      else if(this.props.modelHistory[versionId] == 'UpdateParam') {
        msg = 'Updated value of parameter';
      }
      else if(this.props.modelHistory[versionId] == 'ModelShared') {
        msg = 'Shared Model';
      }

      if (this.props.modelHistory[versionId] != 'CheckpointCreated') {
        let link = (<tr key={versionId}>
                      <td>{index + 1}</td>
                      <td>
                        {msg}
                      </td>
                      <td>
                        <a id={versionId} href={url}>
                          <span className="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                        </a>
                      </td>
                    </tr>);
        data.push(link);
      }
    });

    return (
      <div className="url-import-modal" style={{ paddingTop:'10px'}}>
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Version Id</th>
              <th>Tag</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody>
            {data}
          </tbody>
        </table>
      </div>
    );
  }
}

UpdateHistoryModal.propTypes = {
  networkId: React.PropTypes.number,
  modelHistory: React.PropTypes.object.isRequired,
  addError: React.PropTypes.func
};

export default UpdateHistoryModal;
