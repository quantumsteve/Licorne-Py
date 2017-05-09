from licorne.layer import Layer
from licorne.SampleModel import SampleModel
import numpy as np
import unittest

class TestSampleModelClass(unittest.TestCase):

    def test_creation_addition_deletion(self):
        sm=SampleModel()
        sm.addItem(Layer(name='0'))
        sm.addItem(Layer(name='1'))
        sm.addItem(Layer(name='2'))
        sm.addItem(Layer(name='3'))
        sm.addItem('4') #should have no effect
        expected_names=['incoming media', '0', '1', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.delItem(0)                
        expected_names=['incoming media', '1', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.delItem(3)                
        expected_names=['incoming media', '1', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)

    def test_iterate(self):
        sm=SampleModel()
        sm.addItem(Layer(name='0'))
        sm.addItem(Layer(name='1'))
        sm.addItem(Layer(name='2',thickness=3.14))
        sm.addItem(Layer(name='3'))
        expected_names=['0', '1', '2', '3']
        self.assertEqual([s.name for s in sm],expected_names)
        expected_thickness=[0,0,3.14,0]
        self.assertEqual([s.thickness.value for s in sm],expected_thickness)
        for i,layer in enumerate(sm):
            layer.nsld=3*i+4j
        for i in range(4):
            self.assertEqual(sm.layers[i].nsld_real.value,3*i)
            self.assertEqual(sm.layers[i].nsld_imaginary.value,4)

    def test_move_up_1(self):
        sm=SampleModel()
        sm.addItem(Layer(name='0'))
        sm.addItem(Layer(name='1'))
        sm.addItem(Layer(name='2'))
        sm.addItem(Layer(name='3'))
        sm.move_up_1([0]) #cannot move up more
        expected_names=['incoming media', '0', '1', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.move_up_1([1])
        expected_names=['incoming media', '1', '0', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.move_up_1([1,2])
        expected_names=['incoming media', '0', '2', '1', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.move_up_1([1,2,4]) #no effect
        expected_names=['incoming media', '0', '2', '1', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)

    def test_move_down_1(self):
        sm=SampleModel()
        sm.addItem(Layer(name='0'))
        sm.addItem(Layer(name='1'))
        sm.addItem(Layer(name='2'))
        sm.addItem(Layer(name='3'))
        sm.move_down_1([3]) #cannot move down more
        expected_names=['incoming media', '0', '1', '2', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.move_down_1([1])
        expected_names=['incoming media', '0', '2', '1', '3', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)
        sm.move_down_1([0,2])
        expected_names=['incoming media', '2', '0', '3', '1', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)

        sm.move_up_1([1,2,4]) #no effect
        expected_names=['incoming media', '2', '0', '3', '1', 'substrate']
        self.assertEqual([s.name for s in [sm.incoming_media]+sm.layers+[sm.substrate]],
                         expected_names)


if __name__ == '__main__':
    unittest.main()
