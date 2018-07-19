import React from 'react';

class UpdateHistoryModal extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    let data = [];

    Object.keys(this.props.modelHistory).sort().reverse().forEach((versionId, index) => {
      let url = 'http://localhost:8000/load?id=' + this.props.networkId + '&version=' + versionId;
      let link = (<tr key={versionId}>
                    <td>{index + 1}</td>
                    <td>
                      {this.props.modelHistory[versionId]}
                    </td>
                    <td>
                      <a id={versionId} href={url}>
                        <span className="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                      </a>
                    </td>
                  </tr>);

      data.push(link);
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
