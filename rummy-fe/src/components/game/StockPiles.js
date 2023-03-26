import { Row, Col, Collapse, Card } from "antd"
import styles from './Game.module.css'

const StockPiles = (props) => {
    const { Panel } = Collapse;
    const stockPileCards = () => {
        let rows = []
        for(let i=0; i <= 51; i++) {
            rows.push(<Panel  key={i} className={styles.small_pane} collapsible="disabled" showArrow={false} >
            </Panel> )
        }
        return rows
    }
    return (
        <Row>
        <Col span={24}>
        <Card title="Stock pile" bordered={false}>
            <Collapse accordion={true} defaultActiveKey={54}>
                {stockPileCards()}
                <Panel  key={54}>
                    {/* <button>Draw</button> */}
                </Panel>  
            </Collapse>
        </Card>
        </Col>
        <Col span={24}> 
            <Card title="Discard pile" bordered={false}>
                <Collapse accordion={true} defaultActiveKey={5}>
                    <Panel  key="1" className={styles.small_pane} collapsible="disabled" showArrow={false} >
                    </Panel> 
                    <Panel key="2" className={styles.small_pane} collapsible="disabled" showArrow={false} >
                    </Panel> 
                    <Panel  key="3" className={styles.small_pane} collapsible="disabled" showArrow={false} >
                    </Panel> 
                    <Panel  key="4" className={styles.small_pane} collapsible="disabled" showArrow={false} >
                    </Panel>  
                    <Panel header="&clubs; A" key={5}>
                        {/* <button>Draw</button> */}
                    </Panel>  
                </Collapse>
            </Card>
        </Col>
        </Row>
    )
}

export default StockPiles;